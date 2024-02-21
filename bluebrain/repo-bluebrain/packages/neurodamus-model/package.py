##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import llnl.util.tty as tty

from contextlib import contextmanager

from spack.package import *

from .py_neurodamus import PyNeurodamus

# Definitions
_CORENRN_MODLIST_FNAME = "coreneuron_modlist.txt"
_BUILD_NEURODAMUS_FNAME = "build_neurodamus.sh"
PYNEURODAMUS_DEFAULT_V = PyNeurodamus.LATEST_STABLE
COMMON_DEFAULT_V = "2.8.1"


def version_from_model_ndpy_dep(
    model_v, ndamus_v=PYNEURODAMUS_DEFAULT_V, common_v=COMMON_DEFAULT_V
):
    """New version scheme following dependency on neurodamus-py and common"""
    this_version = model_v + "-" + ndamus_v + "-" + common_v  # e.g. 1.1-3.0.2-2.6.4
    version(this_version, tag=model_v, submodules=True, get_full_repo=True)
    depends_on("py-neurodamus@" + ndamus_v, type=("build", "run"), when="@" + this_version)


class NeurodamusModel(Package):
    """An 'abstract' base package for Simulation Models. Therefore no version.
    Eventually in the future Models are independent entities,
    not tied to neurodamus
    """

    variant("coreneuron", default=True, description="Enable CoreNEURON Support")
    variant("caliper", default=False, description="Enable Caliper instrumentation")

    # NOTE: Several variants / dependencies come from SimModel
    variant(
        "common_mods",
        default="default",
        description="Source of common mods. '': no change, other string: alternate path",
    )

    resource(
        name="common_mods",
        git="ssh://git@bbpgitlab.epfl.ch/hpc/sim/models/common.git",
        tag=COMMON_DEFAULT_V,
        destination="common_latest",
    )

    # Now we depend on neurodamus-py
    # However don't depend on it at runtime just yet, we still want to use
    # use neurodamus-py from GCC stack for compatibility with other Python
    # libs (bglibpy)
    depends_on("py-neurodamus@develop", type=("build", "run"), when="@develop")

    # Note: We dont request link to MPI so that mpicc can do what is best
    # and dont rpath it so we stay dynamic.
    # 'run' mode will load the same mpi module
    depends_on("mpi", type=("build", "run"))

    depends_on("hdf5+mpi")
    depends_on("libsonata-report")

    # neuron/corenrn get linked automatically when using nrnivmodl[-core]
    # Dont duplicate the link dependency (only 'build' and 'run')
    depends_on("neuron+mpi", type=("build", "run"))
    depends_on("neuron+coreneuron+python", type=("build", "run"), when="+coreneuron")
    depends_on("neuron+caliper", when="+caliper", type=("build", "run"))
    depends_on("gettext", when="^neuron")

    mech_name = None

    @property
    def lib_suffix(self):
        return ("_" + self.mech_name) if self.mech_name else ""

    @property
    def nrnivmodl_core_exe(self):
        """
        TODO: this is temporary change until we move to 9.0a soon.
        """
        if self.spec.satisfies("^coreneuron") and self.spec["neuron"].satisfies("@:8.99"):
            return which("nrnivmodl-core", path=self.spec["coreneuron"].prefix.bin, required=True)
        else:
            return which("nrnivmodl-core", path=self.spec["neuron"].prefix.bin, required=True)

    def _coreneuron_include_flag(self):
        if self.spec.satisfies("^coreneuron"):
            return " -DENABLE_CORENEURON" + " -I%s" % self.spec["coreneuron"].prefix.include
        else:
            return " -DENABLE_CORENEURON" + " -I%s" % self.spec["neuron"].prefix.include

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

    def setup_build_environment(self, env):
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

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        # We will find 0 or 1 lib
        for libnrnmech_name in find(self.prefix.lib, "libnrnmech*.so", recursive=False):
            env.prepend_path("BLUECELLULAB_MOD_LIBRARY_PATH", libnrnmech_name)

    # NOTE: With Spack chain we no longer require support for external libs.
    # However, in some setups (notably tests) some libraries might still be
    # specificed as external and, if static,
    # and we must bring their dependencies.
    depends_on("zlib")  # for hdf5

    phases = ["setup_common_mods", "merge_hoc_mod", "build", "install"]

    def setup_common_mods(self, spec, prefix):
        """Setup common mod files if provided through variant."""
        # If specified common_mods then we must change the source
        # Particularly useful for CI of changes to models/common
        if spec.variants["common_mods"].value != "default":
            shutil.move("common", "_common_orig")
            force_symlink(spec.variants["common_mods"].value, "common")
        elif spec.satisfies("@1.6:"):
            # From v1.6 on all models require external common
            tty.info("Using Latest common")
            force_symlink("common_latest/common", "common")

    def merge_hoc_mod(self, spec, prefix):
        """Add hocs, mods and python scripts from neurodamus-core which comes
        as a submodule of py-neurodamus.

        This routine simply adds the additional mods to existing dirs
        so that incremental builds can actually happen.
        """
        core = spec["py-neurodamus"]
        core_prefix = core.prefix

        # If we shall build mods for coreneuron,
        # only bring from core those specified
        if spec.satisfies("+coreneuron"):
            shutil.copytree("mod", "mod_core", True)
            core_nrn_mods = set()
            with open(core_prefix.lib.mod.join(_CORENRN_MODLIST_FNAME)) as core_mods:
                for aux_mod in core_mods:
                    mod_fil = core_prefix.lib.mod.join(aux_mod.strip())
                    if os.path.isfile(mod_fil):
                        shutil.copy(mod_fil, "mod_core")
                        core_nrn_mods.add(aux_mod.strip())
            with working_dir(core_prefix.lib.mod):
                all_mods = set(f for f in os.listdir() if f.endswith(".mod"))
            with open(join_path("mod", "neuron_only_mods.txt"), "w") as blackl:
                blackl.write("\n".join(all_mods - core_nrn_mods) + "\n")

        # Neurodamus model may not have python scripts
        mkdirp("python")

        copy_all(core_prefix.lib.hoc, "hoc", make_link)
        copy_all(core_prefix.lib.mod, "mod", make_link)
        copy_all(core_prefix.lib.python, "python", make_link)

    def build(self, spec, prefix):
        """Build mod files from with nrnivmodl / nrnivmodl-core.
        To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        # Create the library with all the mod files as libnrnmech.so/.dylib
        self.mech_name = ""

        build_script_parameters = {}

        mods_location = "mod"
        link_flag = ""
        include_flag = ""
        corenrn_mods = "mod_core"
        # pass include and link flags for all dependency libraries
        # Compiler wrappers are not used to have a more reproducible building
        for dep_spec in self.spec.dependencies(deptype="link"):
            dep = self.spec[dep_spec.name]
            link_flag += " {0} {1}".format(
                dep.libs.ld_flags, " ".join(["-Wl,-rpath," + x for x in dep.libs.directories])
            )
            include_flag += " -I " + str(dep.prefix.include)

        output_dir = os.path.basename(self.spec["neuron"].package.archdir)

        build_script_parameters["incflags"] = include_flag
        build_script_parameters["loadflags"] = link_flag

        if self.spec.satisfies("+coreneuron"):
            mods_location = os.path.abspath(corenrn_mods or mods_location)
            assert os.path.isdir(mods_location) and find(mods_location, "*.mod", recursive=False), (
                "Invalid mods dir: " + mods_location
            )
            nrnivmodl_params = ["-n", "ext", "-i", include_flag, "-l", link_flag]
            with working_dir("build_" + self.mech_name, create=True):
                force_symlink(mods_location, "mod")
                self.nrnivmodl_core_exe(*(nrnivmodl_params + ["mod"]))
                output_dir = os.path.basename(self.spec["neuron"].package.archdir)
                mechlib = find_libraries("libcorenrnmech_ext*", output_dir)
                assert len(mechlib.names) == 1, "Error creating corenrnmech. Found: " + str(
                    mechlib.names
                )
            libnrncoremech = mechlib
            # Relevant flags to build neuron's nrnmech lib
            # 'ENABLE_CORENEURON' only now, otherwise mods assume neuron
            # Only link with coreneuron when dependencioes are passed
            include_flag += self._coreneuron_include_flag()
            link_flag += " " + libnrncoremech.ld_flags

        # Neuron mechlib and special
        with profiling_wrapper_on():
            link_flag += " -L{0} -Wl,-rpath,{0}".format(str(self.prefix.lib))
            which("nrnivmodl")("-incflags", include_flag, "-loadflags", link_flag, mods_location)

        assert os.path.isfile(os.path.join(output_dir, "special"))

        # Create rebuild script
        if spec.satisfies("+coreneuron"):
            nrnivmodlcore_call = str(self.nrnivmodl_core_exe)
            nrnivmodl_params = ["-n", "ext", "-i", include_flag, "-l", link_flag]
            for param in nrnivmodl_params:
                nrnivmodlcore_call += " '%s'" % param
            include_flag += " " + self._coreneuron_include_flag()
        else:
            nrnivmodlcore_call = ""

        with open(_BUILD_NEURODAMUS_FNAME, "w") as f:
            f.write(
                _BUILD_NEURODAMUS_TPL.format(
                    nrnivmodl=str(which("nrnivmodl")),
                    incflags=include_flag,
                    loadflags=link_flag,
                    nrnivmodlcore_call=nrnivmodlcore_call,
                )
            )
        os.chmod(_BUILD_NEURODAMUS_FNAME, 0o770)

    def install(self, spec, prefix):
        """Install phase.

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        python/ If neurodamus-core comes with python, create links
        """
        # base dest dirs already created by model install
        # We install binaries normally, except lib has a suffix
        self._install_binaries()

        # Install mods/hocs, and a builder script
        self._install_src(prefix)
        shutil.move(_BUILD_NEURODAMUS_FNAME, prefix.bin)

        # Create mods links in share
        core = spec["py-neurodamus"]
        force_symlink(core.prefix.lib.mod, prefix.share.mod_neurodamus)
        force_symlink(prefix.lib.mod, prefix.share.mod_full)

        filter_file(
            r"UNKNOWN_NEURODAMUS_MODEL", r"%s" % spec.name, prefix.lib.hoc.join("defvar.hoc")
        )
        filter_file(
            r"UNKNOWN_NEURODAMUS_VERSION", r"%s" % spec.version, prefix.lib.hoc.join("defvar.hoc")
        )

        try:
            commit_hash = self.fetcher[0].get_commit()
        except Exception as e:
            tty.warn(e)
        else:
            filter_file(
                r"UNKNOWN_NEURODAMUS_HASH",
                r"'%s'" % commit_hash[:8],
                prefix.lib.hoc.join("defvar.hoc"),
            )

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        for libnrnmech_name in find(self.prefix.lib, "libnrnmech*", recursive=False):
            # We have the two libs and must export them in different vars
            #  - NRNMECH_LIB_PATH the combined lib (used by neurodamus-py)
            #  - BLUECELLULAB_MOD_LIBRARY_PATH is the pure mechanism
            #        (used by bglib-py)
            if "libnrnmech." in libnrnmech_name:
                env.set("NRNMECH_LIB_PATH", libnrnmech_name)
            else:
                env.set("BLUECELLULAB_MOD_LIBRARY_PATH", libnrnmech_name)


_BUILD_NEURODAMUS_TPL = """#!/bin/sh
set -e
if [ "$#" -eq 0 ]; then
    echo "******* Neurodamus builder *******"
    echo "Syntax:"
    echo "$(basename $0) <mods_dir> [add_include_flags] [add_link_flags]"
    echo
    echo "NOTE: mods_dir is literally passed to nrnivmodl."
    echo "If you only have the mechanism mods"
    echo " and wish to build neurodamus you need to include"
    echo " the neurodamus-specific mods."
    echo " Under \\$NEURODAMUS_ROOT/share you'll find the whole set"
    echo " of original mod files, as"
    echo " well as the neurodamus-specific mods alone."
    echo " You may copy/link them into your directory."
    exit 1
fi

# run with nrnivmodl in path
set -xe

MODDIR=$1
shift

if [ ! -d "$MODDIR" ]; then
    echo "Please provide a valid directory with mod files"
    exit -1
fi

COMPILE_ONLY_NEURON=0

if [[ "$1" == "--only-neuron" ]]; then
    echo "Compiling mechanisms only for NEURON"
    COMPILE_ONLY_NEURON=1
    shift
fi
NRNIVMODL_EXTRA_INCLUDE_FLAGS="$1"
NRNIVMODL_EXTRA_LOAD_FLAGS="$2"

if [ -n "{nrnivmodlcore_call}" ] && [ "$COMPILE_ONLY_NEURON" -eq "0" ]; then
    rm -rf _core_mods
    mkdir _core_mods
    touch "$MODDIR/neuron_only_mods.txt"  # ensure exists
    for f in "$MODDIR"/*.mod; do
        if ! grep $(basename $f) "$MODDIR/neuron_only_mods.txt"; then
            cp $f _core_mods/
        fi
    done
    {nrnivmodlcore_call} _core_mods
    libpath=$(dirname */libcorenrnmech_ext*)
    extra_loadflags="-L $(pwd)/$libpath -lcorenrnmech_ext -Wl,-rpath=\\$ORIGIN"

    echo "Your build supports CoreNeuron. However in some systems
        the coreneuron mods might not be loadable without a location hint.
        In case you get an error such as
            'libcorenrnmech_ext.so: cannot open shared object file
        please run the command:
            export LD_LIBRARY_PATH=$libpath:\\$LD_LIBRARY_PATH"
fi

'{nrnivmodl}' -incflags '{incflags} '"$NRNIVMODL_EXTRA_INCLUDE_FLAGS" -loadflags \
    '{loadflags} '"$extra_loadflags $NRNIVMODL_EXTRA_LOAD_FLAGS" "$MODDIR"

# Final Cleanup
if [ -d _core_mods ]; then
    rm -rf _core_mods
fi
"""


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
