# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack


class PyBglibpy(spack.PythonPackage):
    """Pythonic Blue Brain simulator access"""
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/sim/BGLibPy"
    git = "ssh://bbpcode.epfl.ch/sim/BGLibPy"

    spack.version('develop', branch='master')
    spack.version(
        '4.0.27',
        commit='42d9c1f891ef1ec9af6d72c49ff3b7726a009951',
        preferred=True)

    spack.depends_on('py-setuptools', type=('build', 'run'))

    spack.depends_on('neuron+python~mpi', type='run')
    spack.depends_on('py-h5py~mpi@2.3:', type='run')

    spack.depends_on('py-bluepy@0.13.2:', type='run')
