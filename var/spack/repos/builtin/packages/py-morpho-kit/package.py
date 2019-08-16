# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphoKit(PythonPackage):
    """Python library for reading / writing morphology files"""

    homepage = "https://bbpcode.epfl.ch/code/#/projects/nse/morpho-kit,dashboards/default"
    url      = "https://bbpcode.epfl.ch/code/a/nse/morpho-kit"
    git      = "https://bbpcode.epfl.ch/code/a/nse/morpho-kit"

    version('develop', branch='master', submodules=True)

    depends_on('py-setuptools', type='build')

    depends_on('morphio', type=('build', 'link'))

    depends_on('cmake@3.2:', type='build')
    depends_on('py-numpy', type='run')
