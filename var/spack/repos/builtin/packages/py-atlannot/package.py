# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version

class PyAtlannot(PythonPackage):
    """Alignment of brain atlas annotations."""

    homepage = "https://bbpgitlab.epfl.ch/project/proj101/atlas_annotation"
    git = "git@bbpgitlab.epfl.ch:project/proj101/atlas_annotation.git"

    maintainers = ['EmilieDel', 'Stannislav']

    version('0.1.0', commit='f5c1746013a03f71846d4da6d2c47b515a824b79')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-antspyx@0.2.7', type=('run'))
    depends_on('py-matplotlib', type=('run'))
    depends_on('py-numpy', type=('run'))

