# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCwlRegistry(PythonPackage):
    """Workflows registered in CWL format
    """
    homepage = "https://bbpgitlab.epfl.ch/nse/cwl-registry"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/cwl-registry.git"

    version('develop', branch='main')
    version('0.3.0', tag='cwl-registry-v0.3.0')

    depends_on('python@3.7:', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type=('build', 'run'))

    depends_on("py-click@8.0.0:", type=('build', 'run'))
    depends_on('py-voxcell', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-libsonata', type=('build', 'run'))
    depends_on('py-nexusforge', type=('build', 'run'))
    depends_on('py-bba-data-push', type=('build', 'run'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
