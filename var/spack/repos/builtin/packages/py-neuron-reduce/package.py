# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeuronReduce(PythonPackage):
    """Spack wrapper package for neuron reduction algorithm by Oren Amsalem"""

    homepage = "https://github.com/orena1/neuron_reduce"
    url = "git@github.com:orena1/neuron_reduce.git"
    git = "git@github.com:orena1/neuron_reduce.git"

    version('develop', branch='master')
    version('0.0.6', commit='0c0071f499d2663aa18b8cf1c86c4a3d5a1c3c85')
    version('0.0.7', commit='1bad597f2faa5ff6aa8c94b6f326f86a02e656d7')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.17:', type='run')
    depends_on('neuron+python', type='run')

    def setup_run_environment(self, env):
        env.unset('PMI_RANK')
        env.set('NEURON_INIT_MPI', "0")
