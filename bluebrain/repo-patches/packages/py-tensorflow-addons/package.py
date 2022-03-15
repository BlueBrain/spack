# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorflowAddons(Package):
    """
    TensorFlow Addons is a repository of contributions that conform to
    well-established API patterns, but implement new functionality not
    available in core TensorFlow. TensorFlow natively supports a large number
    of operators, layers, metrics, losses, and optimizers. However, in a fast
    moving field like ML, there are many interesting new developments that
    cannot be integrated into core TensorFlow (because their broad
    applicability is not yet clear, or it is mostly used by a smaller subset
    of the community).
    """

    homepage = "https://pypi.org/project/tensorflow-addons/"
    url = "https://files.pythonhosted.org/packages/2d/9a/c917382f0145c4c5cd0ce6643225fbd2d49a67bfce5b7a34a342d6837d4d/tensorflow_addons-0.16.1-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl"

    version('0.16.1', sha256='23c822eaaed2d0024c6e9d8e487c472d947553d410cfbcdfb6fadcab2151d3e6', expand=False)

    maintainers = ['pramodk']
    import_modules = ['tensorflow_addons']

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-setuptools', type='build')
    depends_on('py-tensorflow@2.6.0:2.8.999', type=('build', 'run'))
    depends_on('py-typeguard@2.7:', type=('build', 'run'))
    # no versions for Mac OS added
    conflicts('platform=darwin', msg='macOS is not supported')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        with working_dir('spack-test', create=True):
            for module in self.import_modules:
                python('_c', 'import {0}'.format(module))
