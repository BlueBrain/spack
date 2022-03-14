# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlasSplitter(PythonPackage):
    """CLI to split atlas regions and modify annotations accordingly"""
    homepage = "https://github.com/BlueBrain/atlas-splitter"
    git      = "git@github.com/BlueBrain/atlas-splitter.git"

    version('0.1.1', tag='v0.1.1')

    depends_on('py-atlas-commons@0.1.4:', type=('build', 'run'))
    depends_on('py-cgal-pybind@0.1.1:', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-voxcell@3.0.0:', type=('build', 'run'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/test_app_layer_splitter.py")
