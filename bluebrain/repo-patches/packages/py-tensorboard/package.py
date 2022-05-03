from spack import *
from spack.pkg.builtin.py_tensorboard import PyTensorboard as BuiltinPyTensorboard


class PyTensorboard(BuiltinPyTensorboard):
    __doc__ = BuiltinPyTensorboard.__doc__

    patch('bazel-5.patch', when='^bazel@5:')

    # Needs to be copied due to `bazel` being created weirdly
    def build(self, spec, prefix):
        bazel('--nohome_rc',
              '--nosystem_rc',
              '--output_user_root=' + self.tmp_path,
              'build',
              # watch https://github.com/bazelbuild/bazel/issues/7254
              '--define=EXECUTOR=remote',
              '--verbose_failures',
              '--spawn_strategy=local',
              '--subcommands=pretty_print',
              '--jobs={0}'.format(make_jobs),
              '//tensorboard/pip_package')
