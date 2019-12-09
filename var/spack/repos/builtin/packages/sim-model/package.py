# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from llnl.util import tty

from contextlib import contextmanager
import os
import shutil


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
        git = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"
        version('develop', branch='master')
    ```

    Nevertheless, for them to become full neurodamus packages, they may inherit from
    NeurodamusModel instead. See neurodamus-xxx packages for examples.

    """
    variant('coreneuron',  default=False, description="Enable CoreNEURON Support")
    variant('profile',     default=False, description="Enable profiling using Tau")

    # We dont link automatically to neuron/corenrn, nrnivmodl does it for us (=> no 'link' mode)
    depends_on('neuron+mpi', type=('build', 'run'))
    depends_on('coreneuron', when='+coreneuron', type=('build', 'run'))
    depends_on('coreneuron+profile', when='+coreneuron+profile')
    depends_on('neuron+profile', when='+profile')
    depends_on('tau', when='+profile')

    conflicts('^neuron~python', when='+coreneuron')

    phases = ('build', 'install')

    mech_name = None
    """The name of the mechanism, defined in subclasses"""

    def build(self, spec, prefix):
        """Build phase"""
        self._build_mods('mod')

    @property
    def lib_suffix(self):
        return ('_' + self.mech_name) if self.mech_name else ''

    def _build_mods(self, mods_location, link_flag='', include_flag='', corenrn_mods=None):
        """Build shared lib & special from mods in a given path
        """
        # pass include and link flags for all dependency libraries
        # Compiler wrappers are not used to have a more reproducible building
        dep_names = set(self.spec.dependencies_dict('link').keys())
        for dep in dep_names:
            if self.spec[dep].prefix in ('/usr', '/usr/local'):
                raise Exception('Dependency lib "' + dep + '" coming from system prefix')
        link_flag += ' ' + ' '.join(self.spec[dep].libs.ld_flags for dep in dep_names)
        link_flag += ' ' + ' '.join(self.spec[dep].libs.rpath_flags for dep in dep_names)
        include_flag += ' ' + ' '.join(self.spec[dep].headers.include_flags for dep in dep_names)
        include_flag += ' -DENABLE_TAU_PROFILER' if '+profile' in self.spec else ''
        output_dir = os.path.basename(self.neuron_archdir)

        if self.spec.satisfies('+coreneuron'):
            libnrncoremech = self.__build_mods_coreneuron(
                corenrn_mods or mods_location, link_flag, include_flag
            )
            # Relevant flags to build neuron's nrnmech lib
            include_flag += ' -DENABLE_CORENEURON'  # only now, otherwise mods assume neuron
            link_flag += ' ' + libnrncoremech.ld_flags

        # Neuron mechlib and special
        with profiling_wrapper_on():
            link_flag += ' -Wl,-rpath,' + self.prefix.lib
            which('nrnivmodl')('-incflags', include_flag, '-loadflags', link_flag, mods_location)

        assert os.path.isfile(os.path.join(output_dir, 'special'))
        return include_flag, link_flag

    def __build_mods_coreneuron(self, mods_location, link_flag, include_flag):
        spec = self.spec
        assert os.path.isdir(mods_location), 'Invalid mods dir: ' + mods_location
        nrnivmodl_params = ['-n', self.mech_name,
                            '-i', include_flag,
                            '-l', link_flag,
                            '-V',
                            mods_location]
        with working_dir('build_' + self.mech_name, create=True):
            which('nrnivmodl-core')(*nrnivmodl_params)
            output_dir = os.path.basename(self.neuron_archdir)
            mechlib = find_libraries('libcorenrnmech' + self.lib_suffix + '*', output_dir)
            assert len(mechlib.names) == 1, 'Error creating corenrnmech. Found: ' + str(mechlib.names)
        return mechlib

    def install(self, spec, prefix, install_src=True):
        """Install phase

        bin/ <- special and special-core
        libs/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        """
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.share.modc)

        self._install_binaries()

        if install_src:
            self._install_src(prefix)

    def _install_binaries(self, mech_name=None):
        # Install special
        mech_name = mech_name or self.mech_name
        arch = os.path.basename(self.neuron_archdir)
        prefix = self.prefix

        if self.spec.satisfies('+coreneuron'):
            with working_dir('build_' + mech_name):
                if self.spec.satisfies('^coreneuron@0.14:0.16.99'):
                    which('nrnivmech_install.sh', path=".")(prefix)
                elif self.spec.satisfies('^coreneuron@0.17:'):
                    which('nrnivmodl-core')("-d", prefix)  # Set dest to install

        # Install special
        shutil.copy(join_path(arch, 'special'), prefix.bin)

        if self.spec.satisfies('^neuron~binary'):
            # Install libnrnmech - might have several links.
            for f in find(arch + '/.libs', 'libnrnmech*.so*', recursive=False):
                if not os.path.islink(f):
                    bname = os.path.basename(f)
                    lib_dst = prefix.lib.join(bname[:bname.find('.')] + self.lib_suffix + '.so')
                    shutil.move(f, lib_dst)  # Move so its not copied twice
                    break
            else:
                raise Exception('No libnrnmech found')

            # Patch special for the new libname
            which('sed')('-i.bak',
                         's#-dll .*#-dll %s "$@"#' % lib_dst,
                         prefix.bin.special)
            os.remove(prefix.bin.join('special.bak'))

    def _install_src(self, prefix):
        """Copy original and translated c mods
        """
        arch = os.path.basename(self.neuron_archdir)
        mkdirp(prefix.lib.mod, prefix.lib.hoc, prefix.lib.python)
        copy_all('mod', prefix.lib.mod)
        copy_all('hoc', prefix.lib.hoc)
        if os.path.isdir('python'):
            copy_all('python', prefix.lib.python)  # Recent neurodamus
        else:
            shutil.copy('hoc/mapping.py', prefix.lib.python)

        for cmod in find(arch, '*.c', recursive=False):
            shutil.move(cmod, prefix.share.modc)

    def setup_environment(self, spack_env, run_env):
        spack_env.unset('LC_ALL')
        # Remove LD_LIB_PATHs
        to_rem = ('LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'DYLD_FALLBACK_LIBRARY_PATH')
        run_env.env_modifications = [envmod for envmod in run_env.env_modifications
                                     if envmod.name not in to_rem]
        run_env.prepend_path('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        run_env.prepend_path('PYTHONPATH', self.prefix.lib.python)
        for libnrnmech_name in find(self.prefix.lib, 'libnrnmech*_nd.so', recursive=False):
            run_env.set('NRNMECH_LIB_PATH', libnrnmech_name)
            run_env.set('BGLIBPY_MOD_LIBRARY_PATH', libnrnmech_name)


@contextmanager
def profiling_wrapper_on():
    os.environ['USE_PROFILER_WRAPPER'] = '1'
    yield
    del os.environ['USE_PROFILER_WRAPPER']
