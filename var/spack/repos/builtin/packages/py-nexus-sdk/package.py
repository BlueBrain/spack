# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNexusSdk(PythonPackage):
    """A Python API to interface with Blue Brain Nexus REST API.
    """
    homepage = "https://github.com/BlueBrain/nexus-python-sdk"
    url = "https://pypi.io/packages/source/n/nexus-sdk/nexus-sdk-0.3.2.tar.gz"

    version('0.3.2', sha256='cd5668a062283410c5ff57a68c218440df607da84e0a813a8c9390611f7212b3')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-puremagic', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-sseclient', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
