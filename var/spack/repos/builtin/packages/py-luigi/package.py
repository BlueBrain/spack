# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigi(PythonPackage):
    """Workflow mgmgt + task scheduling + dependency resolution"""

    homepage = "https://github.com/spotify/luigi"
    url      = "https://pypi.io/packages/source/l/luigi/luigi-3.0.2.tar.gz"

    version('3.0.2', sha256='b4b1ccf086586d041d7e91e68515d495c550f30e4d179d63863fea9ccdbb78eb')

    depends_on('python@3.6:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    depends_on('py-tornado', type=('build', 'run'))

    depends_on('py-python-daemon@:2.1', type=('build', 'run'))
    depends_on('py-python-dateutil@2.7.5:2.99', type=('build', 'run'))

    depends_on('py-pytest@3.3.0:', type='test')
