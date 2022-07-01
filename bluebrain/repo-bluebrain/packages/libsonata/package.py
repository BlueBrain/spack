# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsonata(CMakePackage):
    """
    `libsonata` provides C++ API for reading SONATA Nodes / Edges

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """
    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"

    version('develop', branch='master', submodules=False, get_full_repo=True)
    version('0.1.13', tag='v0.1.13', submodules=False, get_full_repo=True)
    version('0.1.12', tag='v0.1.12', submodules=False, get_full_repo=True)
    version('0.1.11', tag='v0.1.11', submodules=False, get_full_repo=True)
    version('0.1.10', tag='v0.1.10', submodules=False, get_full_repo=True)

    variant('mpi', default=True, description="Enable MPI backend")

    depends_on('cmake@3.3:', type='build')
    depends_on('py-setuptools-scm', type='build', when='@0.1:')
    depends_on('fmt@4.0:')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('catch2', when='@0.1.3:')
    # Version restriction guessed from old deployment
    #
    # No `when` clause, as clingo will penalize new versions with the
    # version penalty from `nlohmann-js` then :(
    depends_on('nlohmann-json@:3.9.1')

    def cmake_args(self):
        result = [
            '-DEXTLIB_FROM_SUBMODULES=OFF',
            '-DSONATA_TESTS=OFF',
        ]
        if self.spec.satisfies('+mpi'):
            result.extend([
                '-DCMAKE_C_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicc
                ),
                '-DCMAKE_CXX_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicxx
                ),
            ])
        return result
