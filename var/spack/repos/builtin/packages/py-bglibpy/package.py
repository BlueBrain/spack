# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBglibpy(PythonPackage):
    """Pythonic Blue Brain simulator access"""
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/sim/BGLibPy"
    url = "ssh://bbpcode.epfl.ch/sim/BGLibPy"
    git = "ssh://bbpcode.epfl.ch/sim/BGLibPy"

    version('develop', branch='master')
    version('4.2.14', commit='ab36dadee66f7ccd65a0ba564b97dfee91e7668b')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('neuron+python', type='run')
    depends_on('py-h5py~mpi@2.3:', type='run')
    depends_on('py-bluepy@0.13.2:', type='run')
    depends_on('py-libsonata', type='run')

    def setup_environment(self, spack_env, run_env):
        run_env.set('NEURON_INIT_MPI', "0")
        run_env.unset('PMI_RANK')
