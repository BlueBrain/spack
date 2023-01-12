# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBbaDataPush(PythonPackage):
    """CLIs that take in input atlas pipeline datasets and push them into Nexus
    """
    homepage = "https://bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_nexus_push"
    git = "ssh://git@bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_nexus_push.git"

    version('1.0.3', tag='v1.0.3')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-nexusforge', type='run')
    depends_on('py-click', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-h5py', type='run')
    depends_on('py-pynrrd', type='run')
    depends_on('py-pyyaml', type='run')
    depends_on('py-pyjwt', type='run')

    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
