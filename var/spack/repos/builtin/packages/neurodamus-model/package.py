# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from contextlib import contextmanager
import shutil
import os
import sys


class NeurodamusModel(Package):
    """An 'abstract' base package for Simulation Models. Therefore no version.
       Eventually in the future Models are independent entities, not tied to neurodamus
    """
    depends_on('neurodamus-core')

    variant('coreneuron', default=False, description="Enable CoreNEURON Support")
    variant('profile',    default=False, description="Enable profiling using Tau")
    variant('python',     default=False, description="Enable Python Neurodamus")
    variant('syntool',    default=True,  description="Enable Synapsetool reader")
    variant('sonata',     default=False, description="Enable Synapsetool with Sonata")
    variant('debug',      default=False, description="Compile in debug mode (-O0)")

    depends_on("boost", when="+syntool")
    depends_on("hdf5+mpi")
    depends_on("mpi")
    depends_on("neuron+mpi")
    depends_on("neuron+mpi+debug", when="+debug")

    depends_on('reportinglib')
    depends_on('synapsetool+mpi', when='+syntool~sonata')
    depends_on('synapsetool+mpi+sonata', when='+syntool+sonata')
    # Indirect deps, req'ed if we use static libs
    depends_on('zlib')
    depends_on('boost@1.55:', when="+syntool")
    depends_on('libsonata+mpi', when='+sonata')

    depends_on('coreneuron', when='+coreneuron')
    depends_on('coreneuron+profile', when='+profile')
    depends_on('coreneuron@plasticity', when='@plasicity')

    depends_on('neuron+profile', when='+profile')
    depends_on('reportinglib+profile', when='+profile')
    depends_on('tau', when='+profile')

    depends_on('python@2.7:',      type=('build', 'run'), when='+python')
    depends_on('py-setuptools',    type=('build', 'run'), when='+python')
    depends_on('py-h5py',          type=('build', 'run'), when='+python')
    depends_on('py-numpy',         type=('build', 'run'), when='+python')
    depends_on('py-enum34',        type=('build', 'run'), when='^python@2.4:2.7.999,3.1:3.3.999')
    depends_on('py-lazy-property', type=('build', 'run'), when='+python')

    # coreneuron support is available for plasticity model
    # and requires python support in neuron
    #conflicts('@hippocampus', when='+coreneuron')
    #conflicts('@master', when='+coreneuron')
    conflicts('^neuron~python', when='+coreneuron')
    conflicts('+sonata', when='~syntool')

    # Note : to support neuron as external package where readline is not brought
    # with correct library path
    depends_on('readline')

    phases = ['merge_hoc_mod', 'build', 'install']

    # These vars can be overriden by subclasses to specify additional sources
    # This is required since some models have several sources, e.g.: thalamus
    # By default they use common (which should come from submodule)
    _hoc_srcs = ('common/hoc', 'hoc')
    _mod_srcs = ('common/mod', 'mod')

    @staticmethod
    def copy_all(src, dst, copyfunc=shutil.copy):
        isdir = os.path.isdir
        for name in os.listdir(src):
            pth = join_path(src, name)
            isdir(pth) or copyfunc(pth, dst)

    def merge_hoc_mod(self, spec, prefix):
        # First Initialize with core hoc / mods
        copy_tree(spec['neurodamus-core'].prefix.hoc, 'hoclib')
        copy_tree(spec['neurodamus-core'].prefix.mod, 'modlib')
        # Copy from the several sources
        for hoc_src in self._hoc_srcs:
            self.copy_all(hoc_src, 'hoclib')
        for mod_src in self._mod_srcs:
            self.copy_all(mod_src, 'modlib')

    def build(self, spec, prefix):
        """ Build mod files from m dir
        """
        force_symlink('modlib', 'm')
        dep_libs = ['reportinglib', 'hdf5',  'zlib']
        profile_flag = '-DENABLE_TAU_PROFILER' if '+profile' in spec else ''

        # Allow deps to not recurs bring their deps
        link_flag = '-Wl,--as-needed' if sys.platform != 'darwin' else ''
        include_flag = ' -I%s -I%s %s' % (spec['reportinglib'].prefix.include,
                                          spec['hdf5'].prefix.include,
                                          profile_flag)
        if '+syntool' in spec:
            include_flag += ' -DENABLE_SYNTOOL -I ' + spec['synapsetool'].prefix.include
            dep_libs.append('synapsetool')
        if '+coreneuron' in spec:
            include_flag += ' -DENABLE_CORENEURON -I%s' % (spec['coreneuron'].prefix.include)
            dep_libs.append('coreneuron')

        # link_flag. If shared use -rpath, -L, -l, otherwise lib path
        for dep in dep_libs:
            if spec[dep].satisfies('+shared'):
                link_flag += " %s %s" % (spec[dep].libs.rpath_flags, spec[dep].libs.ld_flags)
            else:
                link_flag += " " + spec[dep].libs.joined()
        if spec.satisfies('+syntool') and spec.satisfies('^synapsetool~shared'):
            link_flag += ' ' + spec['synapsetool'].package.dependency_libs(spec).joined()

        nrnivmodl = which('nrnivmodl')
        with profiling_wrapper_on():
            nrnivmodl('-incflags', include_flag, '-loadflags', link_flag, 'm')
        special = os.path.join(os.path.basename(self.neuron_archdir), 'special')
        assert os.path.isfile(special)

    def install(self, spec, prefix):
        """ Move libs to destination.
            Libs are sym-linked. Compiled libs into libs, special into bin
        """
        mkdirp(prefix.lib)
        shutil.move('modlib', prefix.lib.mod)
        shutil.move('hoclib', prefix.lib.hoc)
        os.makedirs(prefix.lib.modc)
        os.makedirs(prefix.bin)

        if spec.satisfies('+python'):
            # assert  os.path.isdir(neurodamus_core.python)
            os.symlink(spec['neurodamus-core'].prefix.python, prefix.python)

        arch = os.path.basename(self.neuron_archdir)
        shutil.move(join_path(arch, 'special'), prefix.bin)

        # Copy c mods
        for cmod in find(arch, "*.c", recursive=False):
            shutil.move(cmod, prefix.lib.modc)

        # Handle non-binary special
        if os.path.exists(arch + "/.libs/libnrnmech.so"):
            shutil.move(arch + "/.libs/libnrnmech.so", prefix.lib)
            sed = which('sed')
            sed('-i', 's#-dll .*#-dll %s#' % prefix.lib.join('libnrnmech.so'), prefix.bin.special)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        if os.path.isdir(self.prefix.python):
            for m in spack_env.env_modifications:
                if m.name == 'PYTHONPATH':
                    run_env.prepend_path('PYTHONPATH', m.value)
            run_env.prepend_path('PYTHONPATH', self.prefix.python)
            run_env.set('NEURODAMUS_PYTHON', self.prefix.python)


@contextmanager
def profiling_wrapper_on():
    os.environ["USE_PROFILER_WRAPPER"] = "1"
    yield
    del os.environ["USE_PROFILER_WRAPPER"]
