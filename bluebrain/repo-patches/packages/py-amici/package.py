# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAmici(PythonPackage):
    """Advanced Multilanguage Interface for CVODES and IDAS"""

    homepage = "https://github.com/AMICI-dev/AMICI"
    pypi     = "amici/amici-0.11.28.tar.gz"

    version('0.11.28', sha256='a8ddda70d8ebdc40600b4ad2ea02eb26e765ca0e594b957f61866b8c84255d5b')

    depends_on('cmake', type='build')

    depends_on('blas')
    depends_on('boost')
    depends_on('hdf5+hl')
    depends_on('swig')

    depends_on('sbml+python', type=('build', 'run'))
    depends_on('py-sympy', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pkgconfig', type=('build', 'run'))
    depends_on('py-toposort', type=('build', 'run'))
    depends_on('py-wurlitzer', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set("BLAS_LIBS", " ".join(self.spec['blas'].libs))
        env.set("HDF5_BASE", " ".join(self.spec['hdf5'].prefix))
