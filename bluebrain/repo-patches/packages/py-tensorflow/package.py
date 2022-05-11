from spack import *
from spack.pkg.builtin.py_tensorflow import PyTensorflow as BuiltinPyTensorflow
from spack.directives import DirectiveMeta


del BuiltinPyTensorflow.dependencies['bazel']
BuiltinPyTensorflow.versions.clear()


class PyTensorflow(BuiltinPyTensorflow):
    __doc__ = BuiltinPyTensorflow.__doc__

    version(
        '2.7.1',
        sha256='0ed3ac84cda24bed5d24af5e6aeeb595b472fdc530efb9871bc79f830a0cb5f5',
        url='https://files.pythonhosted.org/packages/6c/4e/803c3bfe41270585a95f69023f53f165f8ae4682b648abbdb87595222103/tensorflow-2.7.1-cp39-cp39-manylinux2010_x86_64.whl',
        expand=False,
    )

    depends_on('python@3.9.0:3.9', type=('build', 'run'), when='@2.7.1')

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
