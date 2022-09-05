# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBglibpy(PythonPackage):
    """Pythonic Blue Brain simulator access"""
    homepage = "https://bbpgitlab.epfl.ch/cells/bglibpy"
    git = "ssh://git@bbpgitlab.epfl.ch/cells/bglibpy.git"

    version('develop', branch='main')

    version('4.7.5', commit='0123b49aa98f7287f5076ee53367f846b7ce06d1')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('neuron+python', type='run')

    # dependencies from setup.py
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-matplotlib@3.0.3:', type='run')
    depends_on('py-cachetools', type='run')
    depends_on('py-bluepy@2.4.2:2.999', type='run')
    depends_on('py-bluepy-configfile@0.1.18:', type='run')

    # skip import test, because bglibpy needs HOC_LIBRARY_PATH
    # that could be provided by neurodamus-core
    import_modules = []

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
