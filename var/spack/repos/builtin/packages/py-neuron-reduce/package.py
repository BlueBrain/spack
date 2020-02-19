# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PyNeuronReduce(PythonPackage):
    """Spack wrapper package for neuron reduction algorithm by Oren Amsalem"""

    homepage = "https://github.com/orena1/neuron_reduce"
    url = "https://pypi.org/project/neuron-reduce"
    git = "git@github.com:orena1/neuron_reduce.git"

    version('develop', branch='master')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.17:', type='run')
    depends_on('neuron+python', type='run')

    def setup_environment(self, spack_env, run_env):
        run_env.unset('PMI_RANK')
        run_env.set('NEURON_INIT_MPI', "0")
