from spack import *
from spack.pkg.builtin.darshan_runtime import DarshanRuntime as BuiltinDarshanRuntime


class DarshanRuntime(BuiltinDarshanRuntime):
    __doc__ = BuiltinDarshanRuntime.__doc__

    variant('mmap', default=True, description='Compile with mmap support')

    def configure_args(self):
        config_args = super().configure_args()

        if '+mmap' in self.spec:
            config_args.append('--enable-mmap-logs')

        return config_args
