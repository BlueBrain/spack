##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
from contextlib import contextmanager

from spack.package import *


class SimModel(Package):
    """The base package for building Neuron simulation models .

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

    This recipe is also used by Neurodamus, where the models are extended with
    technical mod files required for auxiliary processes, like loading data.

    """

    homepage = ""

    variant("coreneuron", default=False, description="Enable CoreNEURON Support")
    variant("caliper", default=False, description="Enable Caliper instrumentation")

    # neuron/corenrn get linked automatically when using nrnivmodl[-core]
    # Dont duplicate the link dependency (only 'build' and 'run')
    depends_on("neuron+mpi", type=("build", "run"))
    depends_on("neuron+caliper", when="+caliper", type=("build", "run"))
    depends_on("gettext", when="^neuron+binary")

    conflicts("^neuron~python", when="+coreneuron")
    conflicts("^neuron~coreneuron", when="+coreneuron")

    phases = ("build", "install")

    mech_name = None
    """The name of the mechanism, defined in subclasses"""

    def build(self, spec, prefix):
        """Build phase"""
        self._build_mods("mod")

    @property
    def lib_suffix(self):
        return ("_" + self.mech_name) if self.mech_name else ""

    def _build_mods(
        self, mods_location, link_flag="", include_flag="", corenrn_mods=None, dependencies=None
    ):
        """Build shared lib & special from mods in a given path"""
        if dependencies is None:
            dependencies = self.spec._dependencies_dict("link").keys()
        inc_link_flags = self._raw_compiler_flags(dependencies, include_flag, link_flag)
        output_dir = os.path.basename(self.spec["neuron"].package.archdir)
        include_flag, link_flag = inc_link_flags  # expand to use here with nrnivmodl

        if self.spec.satisfies("+coreneuron"):
            libnrncoremech = self.__build_mods_coreneuron(
                corenrn_mods or mods_location, include_flag, link_flag
            )
            # Additional flags to build Neuron's nrnmechlib w CoreNeuron
            # 'ENABLE_CORENEURON' only now, otherwise mods assume neuron
            # Only link with coreneuron when dependencies are passed
            if dependencies:
                include_flag += " -DENABLE_CORENEURON"
                link_flag += " " + libnrncoremech.ld_flags

        # Neuron mechlib and special
        with profiling_wrapper_on():
            link_flag += " -L{0} -Wl,-rpath,{0}".format(str(self.prefix.lib))
            which("nrnivmodl")("-incflags", include_flag, "-loadflags", link_flag, mods_location)

        assert os.path.isfile(os.path.join(output_dir, "special"))
        return inc_link_flags

    def _raw_compiler_flags(self, dependencies, include_flags="", link_flags=""):
        """Compute include and link flags for all dependency libraries
        Compiler wrappers are not used to have a more reproducible building
        """
        for dep in set(dependencies):
            libs = self.spec[dep].libs
            link_flags += " %s " % libs.ld_flags
            link_flags += " ".join(["-Wl,-rpath," + x for x in libs.directories])
            include_flags += " -I " + str(self.spec[dep].prefix.include)
        return include_flags, link_flags

    @property
    def _nrnivmodlcore_exe(self):
        return which("nrnivmodl-core", path=self.spec["neuron"].prefix.bin, required=True)

    def _nrnivmodlcore_params(self, inc_flags, link_flags):
        return ["-n", "ext", "-i", inc_flags, "-l", link_flags]

    def __build_mods_coreneuron(self, mods_location, include_flag, link_flag):
        mods_location = os.path.abspath(mods_location)
        mod_files = os.path.isdir(mods_location) and find(mods_location, "*.mod", recursive=False)
        assert mod_files, "Invalid mods dir: " + mods_location
        nrnivmodl_params = self._nrnivmodlcore_params(include_flag, link_flag)

        with working_dir("build_" + self.mech_name, create=True):
            force_symlink(mods_location, "mod")
            self._nrnivmodlcore_exe(*(nrnivmodl_params + ["mod"]))
            output_dir = os.path.basename(self.spec["neuron"].package.archdir)
            mechlib = find_libraries("libcorenrnmech_ext*", output_dir)
            assert len(mechlib.names) == 1, "Error creating corenrnmech. Found: %s" % mechlib.names
        return mechlib

    def install(self, spec, prefix, install_src=True):
        """Install phase

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        """
        self._install_binaries()

        if install_src:
            self._install_src(prefix)

    def _install_binaries(self, mech_name=None):
        # Install special
        mkdirp(self.spec.prefix.bin)
        mkdirp(self.spec.prefix.lib)
        mkdirp(self.spec.prefix.share.modc)

        mech_name = mech_name or self.mech_name
        nrnivmodl_outdir = self.spec["neuron"].package.archdir
        arch = os.path.basename(nrnivmodl_outdir)
        prefix = self.prefix

        if self.spec.satisfies("+coreneuron"):
            with working_dir("build_" + mech_name):
                self._nrnivmodlcore_exe("-d", prefix, "-n", "ext", "mod")

        # Install special
        shutil.copy(join_path(arch, "special"), prefix.bin)

        libnrnmech = self._find_install_libnrnmech(nrnivmodl_outdir)

        if self.spec.satisfies("^neuron~binary"):
            # Patch special for the new libname
            which("sed")("-i.bak", 's#-dll .*#-dll %s "$@"#' % libnrnmech, prefix.bin.special)
            os.remove(prefix.bin.join("special.bak"))

    def _find_install_libnrnmech(self, libnrnmech_path):
        """Find and move libnrnmech to final destination"""
        for f in find(libnrnmech_path, "libnrnmech.*", recursive=False):
            if not os.path.islink(f):
                bname = os.path.basename(f)
                lib_dst = self.prefix.lib.join(
                    bname[: bname.find(".")] + self.lib_suffix + "." + dso_suffix
                )
                shutil.move(f, lib_dst)  # Move so its not copied twice
                return lib_dst
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

        for cmod in find(arch, "*.c", recursive=False):
            shutil.move(cmod, prefix.share.modc)

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

        if "+caliper" in self.spec:
            env_set_caliper_flags(env)

    def setup_build_environment(self, env):
        self._setup_build_environment_common(env)

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        # We will find 0 or 1 lib
        for libnrnmech_name in find(self.prefix.lib, "libnrnmech*.so", recursive=False):
            env.prepend_path("BGLIBPY_MOD_LIBRARY_PATH", libnrnmech_name)


@contextmanager
def profiling_wrapper_on():
    os.environ["USE_PROFILER_WRAPPER"] = "1"
    yield
    del os.environ["USE_PROFILER_WRAPPER"]


def env_set_caliper_flags(env):
    env.set("NEURODAMUS_CALI_ENABLED", "true")  # Needed for slurm.taskprolog
    env.set("CALI_MPIREPORT_FILENAME", "/dev/null")  # Prevents 'stdout' output
    env.set("CALI_CHANNEL_FLUSH_ON_EXIT", "true")
    env.set(
        "CALI_MPIREPORT_LOCAL_CONFIG",
        "SELECT sum(sum#time.duration), inclusive_sum(sum#time.duration) GROUP BY prop:nested",
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
    env.set("CALI_MPI_BLACKLIST", "MPI_Comm_rank,MPI_Comm_size,MPI_Wtick,MPI_Wtime")


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
