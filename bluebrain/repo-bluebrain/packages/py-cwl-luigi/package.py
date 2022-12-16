# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCWLLuigi(PythonPackage):
    """Luigi wrapper for CWL workflows
    """
    homepage = "https://bbpgitlab.epfl.ch/nse/cwl-luigi"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/cwl-luigi.git"

    version('develop', branch='main')
    version('0.2.1', tag='cwl-luigi-v0.2.1')

    depends_on('python@3.7:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on("py-click@8.0.0:", type='run')
    depends_on('py-jsonschema@3.2.0:', type='run')
    depends_on('py-luigi', type='run')
    depends_on('py-pyyaml', type='run')
    depends_on('py-cwl-registry', type='run')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
