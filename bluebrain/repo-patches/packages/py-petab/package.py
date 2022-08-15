# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyPetab(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    pypi     = "petab/petab-0.1.29.tar.gz"

    version('0.1.29', sha256='60282fb5ed011e8ed5bbae1a1b3288cce2f0777891ac6af7078487a3acd1f220')
    version('0.1.26', sha256='5d0b1f8581a88b997b5f678559096645c74a825be74f3c89b499d1e84e154ef0')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.15.1:', type=('build', 'run'))
    depends_on('py-pandas@1.2.0:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-python-libsbml@5.17.0:', type=('build', 'run'))
    depends_on('py-sympy', type=('build', 'run'))
    depends_on('py-colorama', type=('build', 'run'))
    depends_on('py-seaborn', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
