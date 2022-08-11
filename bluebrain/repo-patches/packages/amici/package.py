# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack import *


class Amici(CMakePackage):
    """Advanced Multilanguage Interface for CVODES and IDAS"""

    homepage = "https://amici.readthedocs.io/en/latest/"
    url      = "https://github.com/AMICI-dev/AMICI.git"
    git      = "https://github.com/AMICI-dev/AMICI.git"

    version('develop', branch='master')
    version('0.11.32', tag='v0.11.32')
    version('0.11.23', tag='v0.11.23')

    depends_on('blas', type=('build', 'run'))
    depends_on('boost')
    depends_on('hdf5+cxx+hl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('swig', type=('build', 'run'))
    depends_on('mpi')

    depends_on('sundials+klu@5.7.0')

    patch('external-sundials.patch')

    def cmake_args(self):
        args = [
            '-DBUILD_TESTS=OFF'
        ]
        return args

    def setup_build_environment(self, env):
        headers = set(os.path.dirname(h) for h in self.spec['blas'].headers)
        assert len(headers) == 1
        env.set("MKL_INCDIR", next(iter(headers)))
