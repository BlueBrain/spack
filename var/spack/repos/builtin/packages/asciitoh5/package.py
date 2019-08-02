# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.

from spack import *
import shutil
import os

class Asciitoh5(Package):
    """Neurodamus Library necessary to convert from ASCII to H5"""
   
    homepage = "ssh://bbpcode.epfl.ch/sim/utils/asciitoh5"
    git      = "ssh://bbpcode.epfl.ch/sim/utils/asciitoh5"

    version('develop', git=git, branch='master')
    version('0.4', git=git, tag='0.4')
    version('0.2', git=git, tag='0.2')
    version('0.1', git=git, tag='0.1')

    depends_on('neuron~mpi')
    depends_on('hdf5~mpi')

    def install(self, spec, prefix):
	os.mkdir(prefix.lib)
	shutil.copytree('hoc', prefix.lib.hoc)
        shutil.copytree('mod', prefix.lib.mod)
	with working_dir(prefix):
	    link_flag = spec['hdf5'].libs.rpath_flags + ' ' + spec['hdf5'].libs.ld_flags
	    include_flag = ' -I%s' % (spec['hdf5'].prefix.include)
            which('nrnivmodl')('-incflags', include_flag, '-loadflags', link_flag, 'lib/mod')
	    bindir = os.path.basename(self.neuron_archdir)
            special = join_path(bindir, 'special')
            os.mkdir(prefix.bin)
	    shutil.copy(special, prefix.bin)
            for f in find('lib/hoc/neuronHDF5', 'convert.sh'):
                shutil.copy(f, prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.set('HOC_LIBRARY_PATH', self.prefix.lib)
