from spack import *
from spack.pkg.builtin.py_tensorflow import PyTensorflow as BuiltinPyTensorflow


class PyTensorflow(BuiltinPyTensorflow):
    __doc__ = BuiltinPyTensorflow.__doc__

    version(
        '2.7.1',
        sha256='a6df5a8d90f27468d97d0ee0d41c53950a4d6002fdf6d427c0fb0749ab855f60',
        url='https://files.pythonhosted.org/packages/85/0c/0dda0156a38ee79f68c6cced1875d52cedd241e2de09649382778e36850d/tensorflow_gpu-2.7.1-cp39-cp39-manylinux2010_x86_64.whl',
        expand=False,
    )

    depends_on('python@3.9.0:3.9', type=('build', 'run'), when='@2.7.1')
    depends_on('flatbuffers+python@1.12:2', type=('build', 'run'), when='@2.7.1')

    phases = ['install']

    def patch(self):
        pass

    def setup_build_environment(self, env):
        pass

    def install(self, spec, prefix):
        pip = which('pip')
        pip(
            'install',
            '--no-deps',
            self.stage.archive_file,
            '--prefix={0}'.format(prefix)
        )


# And here we butcher stuff with a ragged-edged cleaver
del PyTensorflow.dependencies['bazel']
for v in list(PyTensorflow.versions.keys()):
    if v != Version('2.7.1'):
        del PyTensorflow.versions[v]
PyTensorflow.patches.clear()
