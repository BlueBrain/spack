# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Parpe(CMakePackage):
    """The parPE library provides functionality for solving large-scale parameter
    optimization problems requiring up to thousands of simulations per objective
    function evaluation on high performance computing (HPC) systems.
    """

    homepage = "https://github.com/ICB-DCM/parPE"
    url      = "https://github.com/ICB-DCM/parPE.git"
    git      = "https://github.com/ICB-DCM/parPE.git"

    version('0.4.9', tag='v0.4.9')

    depends_on('amici')
    depends_on('blas')
    depends_on('boost')
    depends_on('ceres-solver')
    depends_on('hdf5')
    depends_on('ipopt+thirdparty-hsl')
    depends_on('mpi')

    depends_on('python')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-sympy', type=('build', 'run'))

    def cmake_args(self):
        args = [
            '-DBUILD_EXAMPLES=OFF',
            '-DBUILD_TESTING=OFF',
        ]
        return args
