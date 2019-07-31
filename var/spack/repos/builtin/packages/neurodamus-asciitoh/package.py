# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.

from spack import *
import shutil
import os

class NeurodamusAsciitoh(Package):
    """Neurodamus Library necessary to convert from ASCII to H5"""
   
    homepage = "ssh://bbpcode.epfl.ch/sim/utils/asciitoh5"
    git      = "ssh://bbpcode.epfl.ch/sim/utils/asciitoh5"

    version('develop', git=git, branch='master')
    version('0.1', git=git, tag='0.1')

    depends_on('neuron~binary+python~mpi')
    depends_on('hdf5~mpi')

    def _get_link_flags(self, lib_name):
        """Helper method to get linking flags similar to spack build, for solid deployments.

        1. static libs passed via full path
        2. shared libs passed with -L -l and RPATH flags
        Attention: This func doesnt handle recursive deps of static libs.
        """
        spec = self.spec[lib_name]
        if spec.satisfies('+shared'):  # Prefer shared if both exist
            return "%s %s" % (spec.libs.rpath_flags, spec.libs.ld_flags)
        return spec.libs.joined()

    def install(self, spec, prefix):
        shutil.copytree('hoc', prefix.hoc)
        shutil.copytree('mod', prefix.mod)
	with working_dir(prefix):
	    link_flag = '-Wl,-rpath,' + self._get_link_flags('hdf5')
	    include_flag = ' -I%s' % (spec['hdf5'].prefix.include)
            which('nrnivmodl')('-incflags', include_flag, '-loadflags', link_flag, 'mod')
	    bindir = os.path.basename(self.neuron_archdir)
            special = join_path(bindir, 'special')
            os.mkdir(prefix.bin)
	    shutil.copy(special, prefix.bin)
            for f in find('hoc/neuronHDF5', 'convert.sh'):
                shutil.copy(f, prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.set('HOC_LIBRARY_PATH', self.prefix.hoc)
