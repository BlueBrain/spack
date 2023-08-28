# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
from contextlib import contextmanager

from llnl.util import tty

from spack.package import *

# Definitions
_BUILD_NEURODAMUS_FNAME = "build_neurodamus.sh"
WITH_CORENEURON = True


class Neurodamus(Package):
    """The next-generation AllInOne Neurodamus deployment.

    Neurodamus includes BBP's simulation suite with all internal sim models.
    """

    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/neurodamus-models"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/sim/neurodamus-models.git"

    version("develop", branch="model_combiner", submodules=True)
    # Let the version scheme be different to avoid mixing with old neurodamus-**?
    # version("2023.05", tag="0.0.2", submodules=True)

    variant("synapsetool", default=True, description="Enable SynapseTool reader (for edges)")
    variant("mvdtool", default=True, description="Enable MVDTool reader (for nodes)")
    variant("caliper", default=False, description="Enable Caliper instrumentation")
    variant("only_synapses", default=True, description="Keep etype mods unmodified")

    # neuron/corenrn get linked automatically when using nrnivmodl[-core]
    # Dont duplicate the link dependency (only 'build' and 'run')
    depends_on("neuron+mpi", type=("build", "run"))
    depends_on("neuron+caliper", when="+caliper", type=("build", "run"))
    depends_on("gettext", when="^neuron+binary")

    depends_on("py-neurodamus", type=("build", "run"))
    # Note: We dont request link to MPI so that mpicc can do what is best
    # and dont rpath it so we stay dynamic.
    # 'run' mode will load the same mpi module
    depends_on("mpi", type=("build", "run"))
    depends_on("hdf5+mpi")
    depends_on("libsonata-report")
    depends_on("synapsetool+mpi", when="+synapsetool")
    depends_on("py-mvdtool+mpi", type="run", when="+mvdtool")
    # NOTE: With Spack chain we no longer require support for external libs.
    # However, in some setups (notably tests) some libraries might still be
    # specificed as external and, if static,
    # and we must bring their dependencies.
    depends_on("zlib")  # for hdf5

    phases = ["build", "install"]

    @run_before("build")
    def merge_hoc_mod(self):
        """Add hocs, mods and python scripts from neurodamus-core which comes
        as a submodule of py-neurodamus.

        This routine simply adds the additional mods to existing dirs
        so that incremental builds can actually happen.
        """
        mm_args = ["--only-synapses"] if self.spec.satisfies("+only_synapses") else []
        which("./model_manager.py")("model_config.json", *mm_args)
        which("ls")("build/ALL/mod", "build/ALL/hoc")

        shutil.move("build/ALL/hoc", ".")
        shutil.move("build/ALL/mod", ".")
        mkdirp("python")

        core_prefix = self.spec["py-neurodamus"].prefix  # Since inclusion of core into nd-py
        copy_all(core_prefix.lib.hoc, "hoc", skip_existing=True)
        copy_all(core_prefix.lib.mod, "mod", skip_existing=True)
        copy_all(core_prefix.lib.python, "python")

    def _build_mods(self, mods_location, link_flag="", include_flag="", dependencies=None):
        """Build shared lib & special from mods in a given path"""
        if dependencies is None:
            dependencies = self.spec._dependencies_dict("link").keys()
        inc_link_flags = self._raw_compiler_flags(dependencies, include_flag, link_flag)
        output_dir = os.path.basename(self.spec["neuron"].package.archdir)
        include_flag, link_flag = inc_link_flags  # expand to use here with nrnivmodl

        # Neuron mechlib and special
        with profiling_wrapper_on():
            link_flag += " -L{0} -Wl,-rpath,{0}".format(str(self.prefix.lib))
            nrnivmodl_args = ["-incflags", include_flag, "-loadflags", link_flag, mods_location]
            if WITH_CORENEURON:
                which("nrnivmodl")("-coreneuron", *nrnivmodl_args)
            else:
                which("nrnivmodl")(*nrnivmodl_args)

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

    def build(self, spec, _prefix):
        """Build mod files from with nrnivmodl / nrnivmodl-core.
        To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        base_include_flag = "-DENABLE_SYNTOOL" if spec.satisfies("+synapsetool") else ""
        include_flag, link_flag = self._build_mods("mod", "", base_include_flag)
        self._create_rebuild_script(include_flag, link_flag)

    def _create_rebuild_script(self, include_flag, link_flag):
        corenrnmech_flag = "-coreneuron" if WITH_CORENEURON else ""

        with open(_BUILD_NEURODAMUS_FNAME, "w") as f:
            f.write(
                _BUILD_NEURODAMUS_TPL.format(
                    nrnivmodl=str(which("nrnivmodl")),
                    incflags=include_flag,
                    loadflags=link_flag,
                    corenrnmech_flag=corenrnmech_flag,
                )
            )
        os.chmod(_BUILD_NEURODAMUS_FNAME, 0o770)

    def _install_binaries(self):
        # Install special
        prefix = self.prefix
        mkdirp(self.spec.prefix.bin)
        mkdirp(self.spec.prefix.lib)
        mkdirp(self.spec.prefix.share.modc)

        # Neuron 9.0 Note:
        #  - We rely on the fact that "nrnivmodl" understands "-coreneuron"
        #    and binaries are generated in a single archdir folder
        nrnivmodl_outdir = self.spec["neuron"].package.archdir

        if WITH_CORENEURON:
            for filename, dest in [("libcorenrnmech.*", prefix.lib), ("special-core", prefix.bin)]:
                f = find(nrnivmodl_outdir, filename, recursive=False)
                assert len(f) == 1, "Could not find " + filename
                shutil.copy(f[0], dest)

        # Install special
        shutil.copy(join_path(nrnivmodl_outdir, "special"), prefix.bin)

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
                lib_dst = self.prefix.lib.join(bname[: bname.find(".")] + "." + dso_suffix)
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

        for cmod in find(arch, "*.cpp", recursive=False):
            shutil.move(cmod, prefix.share.neuron_modcpp)

        if WITH_CORENEURON:
            for cmod in find(arch + "coreneuron/mod2c", "*.cpp", recursive=False):
                shutil.move(cmod, prefix.share.coreneuron_modcpp)

    def install(self, spec, prefix):
        """Install phase.

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        python/ If neurodamus-core comes with python, create links
        """
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

    def setup_build_environment(self, env):
        env.unset("LC_ALL")
        # MPI wrappers know the actual compiler from OMPI_CC or MPICH_CC, which
        # at build-time, are set to compiler wrappers. While that is correct,
        # we dont want for with nrnivmodl since flags have been calculated
        # manually. The chosen way to override those (unknown name) env vars
        # is using setup_run_environment() from the MPI package.
        if "mpi" in self.spec:
            self.spec["mpi"].package.setup_run_environment(env)

    def setup_run_environment(self, env):
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
        # We have to export two different env vars for the neuron library
        #  - NRNMECH_LIB_PATH used by neurodamus-py
        #  - BGLIBPY_MOD_LIBRARY_PATH used by bglibpy
        libnrnmech_name = join_path(self.prefix.lib, "libnrnmech.so")
        env.set("NRNMECH_LIB_PATH", libnrnmech_name)
        # With this unified recipe we are dropping BGLIBPY_MOD_LIBRARY_PATH
        # Since it requires building model a second time without some mechanisms


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


def copy_all(src, dst, copyfunc=shutil.copy, skip_links=False, skip_existing=False):
    """Copy/process all files in a src dir into a destination dir."""
    path = os.path
    for name in os.listdir(src):
        src_pth = join_path(src, name)
        if path.isdir(src_pth) or (skip_links and path.islink(src_pth)):
            continue
        dst_pth = join_path(dst, name)
        if skip_existing and path.exists(dst_pth):
            continue
        copyfunc(src_pth, dst_pth)


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

if [ ! -d "$1" ]; then
    echo "Please provide a valid directory with mod files"
    exit -1
fi

'{nrnivmodl}' '{corenrnmech_flag}' -incflags '{incflags} '"$2" -loadflags \
    '{loadflags} '"$extra_loadflags $3" "$1"

"""
