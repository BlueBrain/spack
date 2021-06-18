# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTensorflow(Package, CudaPackage):
    """TensorFlow is an Open Source Software Library for Machine Intelligence
    """

    homepage = "https://www.tensorflow.org"
    url      = "https://files.pythonhosted.org/packages/9e/ad/c72996e4db140b17f352b9b334dc53304bd62983002d0b01f97ad3733fe2/tensorflow-2.4.2-cp38-cp38-manylinux2010_x86_64.whl"

    maintainers = ['adamjstewart', 'aweits']
    import_modules = ['tensorflow']

    version('2.4.2',  sha256='a768ae4260f62df5e07f9e207b0267fa234cd3c3841c8454e207a9311c9600fc', expand=False)

    extends('python')
    depends_on('python@3:', type=('build', 'run'), when='@2.1:')
    depends_on('py-pip', type='build')

    depends_on('py-numpy@1.16.0:',  type=('build', 'run'), when='@1.15:')
    depends_on('cudnn')
    depends_on('cuda')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        with working_dir('spack-test', create=True):
            for module in self.import_modules:
                python('-c', 'import {0}'.format(module))
