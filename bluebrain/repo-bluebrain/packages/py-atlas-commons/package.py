# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlasCommons(PythonPackage):
    """Library containing common functions to build atlases"""
    homepage = "https://github.com/BlueBrain/atlas-commons"
    git      = "git@github.com/BlueBrain/atlas-commons.git"

    version('0.1.4', tag='v0.1.4')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-voxcell@3.0.0:', type=('build', 'run'))

    depends_on('py-pytest', type='test')
