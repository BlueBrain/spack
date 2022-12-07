from spack.package import *
from spack.pkg.builtin.mxnet import Mxnet as BuiltinMxnet


class Mxnet(BuiltinMxnet):
    __doc__ = BuiltinMxnet.__doc__

    def setup_build_environment(self, env):
        env.set("MKL_ROOT", os.path.dirname(self.spec["intel-oneapi-mkl"].headers[0]))
