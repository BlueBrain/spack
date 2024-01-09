##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
from contextlib import contextmanager

from spack.build_environment import dso_suffix
from spack.package import *


class SimModel(Package):
    """The abstract base package for simulation models.

    Simulation models are groups of nmodl mechanisms. These packages are
    deployed as neuron/coreneuron modules (dynamic loadable libraries)
    which are loadable using load_dll() or linked into a "special"

    Specific models packages can be added to spack by simply inheriting from
    this class and defining basic attributes, e.g.:
    ```
    class ModelHippocampus(SimModel):
        homepage = ""
        git = "ssh://git@bbpgitlab.epfl.ch/hpc/sim/models/hippocampus.git"
        version('develop', branch='master')
    ```

    Nevertheless, for them to become full neurodamus packages, they may inherit
    from NeurodamusModel instead. See neurodamus-xxx packages for examples.

    """

    homepage = ""

    variant("coreneuron", default=True, description="Enable CoreNEURON Support")
    variant("caliper", default=False, description="Enable Caliper instrumentation")

    # neuron/corenrn get linked automatically when using nrnivmodl[-core]
    # Dont duplicate the link dependency (only 'build' and 'run')
    depends_on("neuron+mpi", type=("build", "run"))
    depends_on("neuron+coreneuron+python", type=("build", "run"), when="+coreneuron")
    depends_on("coreneuron", when="+coreneuron ^neuron@:8", type=("build", "run"))
    depends_on("coreneuron+caliper", when="+coreneuron+caliper ^neuron@:8", type=("build", "run"))
    depends_on("neuron+caliper", when="+caliper", type=("build", "run"))
    depends_on("gettext", when="^neuron")

    phases = ("build", "install")

    mech_name = None
    """The name of the mechanism, defined in subclasses"""

    def build(self, spec, prefix):
        """Build phase"""
        self._build_mods("mod")

    @property
    def lib_suffix(self):
        return ("_" + self.mech_name) if self.mech_name else ""

    @property
    def nrnivmodl_core_exe(self):
        """with +coreneuron variant enabled in neuron, nrnivmodl-core
        binary can come from two places: coreneuron or neuron. Depending
        upon the spec that user has used, grab appropriate nrnivmodl-core
        binary. Note that `which` uses $PATH to find out binary and it could
        be "wrong" one i.e. coreneuron built under neuron may not have linked
        with sonatareport.
        TODO: this is temporary change until we move to 9.0a soon.
        """
        if self.spec.satisfies("^coreneuron") and self.spec["neuron"].satisfies("@:8.99"):
            return which("nrnivmodl-core", path=self.spec["coreneuron"].prefix.bin, required=True)
        else:
            return which("nrnivmodl-core", path=self.spec["neuron"].prefix.bin, required=True)

    def _build_mods(self, mods_location, link_flag="", include_flag="", corenrn_mods=None):
        """Build shared lib & special from mods in a given path"""
        # pass include and link flags for all dependency libraries
        # Compiler wrappers are not used to have a more reproducible building
        for dep_spec in self.spec.dependencies(deptype="link"):
            dep = self.spec[dep_spec.name]
            link_flag += " {0} {1}".format(
                dep.libs.ld_flags,
                " ".join(["-Wl,-rpath," + x for x in dep.libs.directories]),
            )
            include_flag += " -I " + str(dep.prefix.include)

        output_dir = os.path.basename(self.spec["neuron"].package.archdir)
        include_flag_raw = include_flag
        link_flag_raw = link_flag

        if self.spec.satisfies("+coreneuron"):
            libnrncoremech = self.__build_mods_coreneuron(
                corenrn_mods or mods_location, link_flag, include_flag
            )
            # Relevant flags to build neuron's nrnmech lib
            # 'ENABLE_CORENEURON' only now, otherwise mods assume neuron
            # Only link with coreneuron when dependencies are passed
            include_flag += self._coreneuron_include_flag()
            link_flag += " " + libnrncoremech.ld_flags

        # Neuron mechlib and special
        with profiling_wrapper_on():
            link_flag += " -L{0} -Wl,-rpath,{0}".format(str(self.prefix.lib))
            which("nrnivmodl")("-incflags", include_flag, "-loadflags", link_flag, mods_location)

        assert os.path.isfile(os.path.join(output_dir, "special"))
        return include_flag_raw, link_flag_raw

    def _nrnivmodlcore_params(self, inc_flags, link_flags):
        return ["-n", "ext", "-i", inc_flags, "-l", link_flags]

    def _coreneuron_include_flag(self):
        if self.spec.satisfies("^coreneuron"):
            return " -DENABLE_CORENEURON" + " -I%s" % self.spec["coreneuron"].prefix.include
        else:
            return " -DENABLE_CORENEURON" + " -I%s" % self.spec["neuron"].prefix.include

    def __build_mods_coreneuron(self, mods_location, link_flag, include_flag):
        mods_location = os.path.abspath(mods_location)
        assert os.path.isdir(mods_location) and find(mods_location, "*.mod", recursive=False), (
            "Invalid mods dir: " + mods_location
        )
        nrnivmodl_params = self._nrnivmodlcore_params(include_flag, link_flag)
        with working_dir("build_" + self.mech_name, create=True):
            force_symlink(mods_location, "mod")
            self.nrnivmodl_core_exe(*(nrnivmodl_params + ["mod"]))
            output_dir = os.path.basename(self.spec["neuron"].package.archdir)
            mechlib = find_libraries("libcorenrnmech_ext*", output_dir)
            assert len(mechlib.names) == 1, "Error creating corenrnmech. Found: " + str(
                mechlib.names
            )
        return mechlib

    def install(self, spec, prefix, install_src=True):
        """Install phase

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod cpp files (modcpp and modcpp_core)
        """
        self._install_binaries()

        if install_src:
            self._install_src(prefix)

    def _install_binaries(self, mech_name=None):
        # Install special
        mkdirp(self.spec.prefix.bin)
        mkdirp(self.spec.prefix.lib)
        mkdirp(self.spec.prefix.share.modcpp)

        mech_name = mech_name or self.mech_name
        nrnivmodl_outdir = self.spec["neuron"].package.archdir
        arch = os.path.basename(nrnivmodl_outdir)
        prefix = self.prefix

        if self.spec.satisfies("+coreneuron"):
            with working_dir("build_" + mech_name):
                if self.spec.satisfies("^coreneuron@0.0:0.14"):
                    raise Exception(
                        "Coreneuron versions before 0.14 are not supported by Neurodamus model"
                    )
                elif self.spec.satisfies("^coreneuron@0.14:0.16.99"):
                    which("nrnivmech_install.sh", path=".")(prefix)
                else:
                    # Set dest to install
                    self.nrnivmodl_core_exe("-d", prefix, "-n", "ext", "mod")

        # Install special
        shutil.copy(join_path(arch, "special"), prefix.bin)

        # Install libnrnmech - might have several links
        libnrnmech_path = nrnivmodl_outdir
        for f in find(libnrnmech_path, "libnrnmech.*", recursive=False):
            if not os.path.islink(f):
                bname = os.path.basename(f)
                lib_dst = prefix.lib.join(
                    bname[: bname.find(".")] + self.lib_suffix + "." + dso_suffix
                )
                shutil.move(f, lib_dst)  # Move so its not copied twice
                break
        else:
            raise Exception("No libnrnmech found")

    def _install_src(self, prefix):
        """Copy original and translated c mods"""
        arch = os.path.basename(self.spec["neuron"].package.archdir)
        mkdirp(prefix.lib.mod, prefix.lib.hoc, prefix.lib.python)
        copy_all("mod", prefix.lib.mod)
        copy_all("hoc", prefix.lib.hoc)
        if os.path.isdir("python"):  # Recent neurodamus
            copy_all("python", prefix.lib.python)

        full_neuron_cpp_generated_files = find(arch, "*.cpp", recursive=False)
        assert (
            len(full_neuron_cpp_generated_files) > 0
        ), "Couldn't find NEURON generated cpp files for mod files"
        for cppmod in full_neuron_cpp_generated_files:
            shutil.move(cppmod, prefix.share.modcpp)
        if self.spec.satisfies("+coreneuron"):
            mkdirp(prefix.share.modcpp_core)
            full_coreneuron_cpp_generated_files = find(
                "build_/" + arch + "/corenrn/mod2c", "*.cpp", recursive=False
            )
            assert (
                len(full_coreneuron_cpp_generated_files) > 0
            ), "Couldn't find CoreNEURON generated cpp files for mod files"
            for core_cppmod in full_coreneuron_cpp_generated_files:
                shutil.move(core_cppmod, prefix.share.modcpp_core)

    def _setup_build_environment_common(self, env):
        env.unset("LC_ALL")
        # MPI wrappers know the actual compiler from OMPI_CC or MPICH_CC, which
        # at build-time, are set to compiler wrappers. While that is correct,
        # we dont want for with nrnivmodl since flags have been calculated
        # manually. The chosen way to override those (unknown name) env vars
        # is using setup_run_environment() from the MPI package.
        if "mpi" in self.spec:
            self.spec["mpi"].package.setup_run_environment(env)

    def _setup_run_environment_common(self, env):
        # Dont export /lib as an ldpath.
        # We dont want to find these libs automatically
        to_rm = ("LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH", "DYLD_FALLBACK_LIBRARY_PATH")
        env.env_modifications = [
            envmod for envmod in env.env_modifications if envmod.name not in to_rm
        ]
        if os.path.isdir(self.prefix.lib.hoc):
            env.set("HOC_LIBRARY_PATH", self.prefix.lib.hoc)
        if os.path.isdir(self.prefix.lib.python):
            env.prepend_path("PYTHONPATH", self.prefix.lib.python)
        env.set("{}_ROOT".format(self.name.upper().replace("-", "_")), self.prefix)

        if "+coreneuron" in self.spec:
            env.set("CORENEURONLIB", self.prefix.lib + "/libcorenrnmech_ext.so")

        # ENV variables to enable Caliper with certain settings
        if "+caliper" in self.spec:
            env.set("NEURODAMUS_CALI_ENABLED", "true")  # Needed for slurm.taskprolog
            env.set("CALI_MPIREPORT_FILENAME", "/dev/null")  # Prevents 'stdout' output
            env.set("CALI_CHANNEL_FLUSH_ON_EXIT", "false")
            env.set(
                "CALI_MPIREPORT_LOCAL_CONFIG",
                "SELECT sum(sum#time.duration), \
                                                        inclusive_sum(sum#time.duration) \
                                                    GROUP BY prop:nested",
            )
            env.set(
                "CALI_MPIREPORT_CONFIG",
                "SELECT annotation, \
                        mpi.function, \
                        min(sum#sum#time.duration) as exclusive_time_rank_min, \
                        max(sum#sum#time.duration) as exclusive_time_rank_max, \
                        avg(sum#sum#time.duration) as exclusive_time_rank_avg, \
                        min(inclusive#sum#time.duration) AS inclusive_time_rank_min, \
                        max(inclusive#sum#time.duration) AS inclusive_time_rank_max, \
                        avg(inclusive#sum#time.duration) AS inclusive_time_rank_avg, \
                        percent_total(sum#sum#time.duration) AS exclusive_time_pct, \
                        inclusive_percent_total(sum#sum#time.duration) AS inclusive_time_pct \
                    GROUP BY prop:nested FORMAT json",
            )
            env.set("CALI_SERVICES_ENABLE", "aggregate,event,mpi,mpireport,timestamp")
            env.set(
                "CALI_MPI_BLACKLIST", "MPI_Comm_rank,MPI_Comm_size,MPI_Wtick,MPI_Wtime"
            )  # Ignore

    def setup_build_environment(self, env):
        self._setup_build_environment_common(env)

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        # We will find 0 or 1 lib
        for libnrnmech_name in find(self.prefix.lib, "libnrnmech*.so", recursive=False):
            env.prepend_path("BLUECELLULAB_MOD_LIBRARY_PATH", libnrnmech_name)


@contextmanager
def profiling_wrapper_on():
    os.environ["USE_PROFILER_WRAPPER"] = "1"
    yield
    del os.environ["USE_PROFILER_WRAPPER"]


def copy_all(src, dst, copyfunc=shutil.copy):
    """Copy/process all files in a src dir into a destination dir."""
    isdir = os.path.isdir
    for name in os.listdir(src):
        pth = join_path(src, name)
        isdir(pth) or copyfunc(pth, dst)


def make_link(src, dst):
    """Create a symlink in a given destination.
    make_link is copy compatible i.e. will take the same args and behave
    similarly to shutil.copy except that it will create a soft link instead.
    If destination is a directory then a new symlink is created inside with
    the same name as the original file.
    Relative src paths create a relative symlink (properly relocated) while
    absolute paths crete an abolute-path symlink.
    If another link already exists in the destination with the same it is
    deleted before link creation.
    Args:
        src (str): The path of the file to create a link to
        dst (str): The link destination path (may be a directory)
    """
    if os.path.isdir(dst):
        dst_dir = dst
        dst = join_path(dst, os.path.basename(src))
    else:
        dst_dir = os.path.dirname(dst)
    if not os.path.isabs(src):
        src = os.path.relpath(src, dst_dir)  # update path relation
    # Silently replace links, just like copy replaces files
    if os.path.islink(dst):
        os.remove(dst)
    os.symlink(src, dst)
