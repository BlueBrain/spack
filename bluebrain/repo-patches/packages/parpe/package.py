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

    patch('fixes-0.4.9.patch')

    depends_on('amici@0.11.23')
    depends_on('blas')
    depends_on('boost')
    depends_on('ceres-solver')
    depends_on('hdf5')
    depends_on('ipopt+thirdparty-hsl')
    depends_on('mpi')

    depends_on('python')
    depends_on('py-setuptools', type=('build',))

    depends_on('py-numpy@1.18.1:', type=('build', 'run'))
    depends_on('py-termcolor', type=('build', 'run'))
    depends_on('py-colorama', type=('build', 'run'))
    depends_on('py-petab@0.1.26', type=('build', 'run'))
    depends_on('py-amici@0.11.23', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-python-libsbml', type=('build', 'run'))
    depends_on('snakemake', type=('build', 'run'))
    depends_on('py-coloredlogs', type=('build', 'run'))

    extends('python')

    def cmake_args(self):
        args = [
            '-DBUILD_EXAMPLES=ON',
            '-DBUILD_TESTING=ON',
        ]
        return args

    def install(self, spec, prefix):
        super().install(spec, prefix)

        with working_dir(join_path(self.stage.source_path, 'python')):
            args = PythonPackage.install_args(self, spec, prefix)
            setup_py("install", *args)
