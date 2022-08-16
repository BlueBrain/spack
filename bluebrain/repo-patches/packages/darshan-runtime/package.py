from spack import *
from spack.pkg.builtin.darshan_runtime import DarshanRuntime as BuiltinDarshanRuntime


class DarshanRuntime(BuiltinDarshanRuntime):
    __doc__ = BuiltinDarshanRuntime.__doc__

    version("3.4.0", sha256="7cc88b7c130ec3b574f6b73c63c3c05deec67b1350245de6d39ca91d4cff0842")

    depends_on('autoconf', type='build', when='@3.4.0:')
    depends_on('automake', type='build', when='@3.4.0:')
    depends_on('libtool',  type='build', when='@3.4.0:')
    depends_on('m4',       type='build', when='@3.4.0:')

    def setup_run_environment(self, env):
        env.set('DARSHAN_LOG_DIR_PATH', "~")
