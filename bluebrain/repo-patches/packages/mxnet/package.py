import os

from spack.package import *
from spack.pkg.builtin.mxnet import Mxnet as BuiltinMxnet


class Mxnet(BuiltinMxnet):
    __doc__ = BuiltinMxnet.__doc__

    version(
        "1.9.1",
        sha256="11ea61328174d8c29b96f341977e03deb0bf4b0c37ace658f93e38d9eb8c9322",
        preferred=True,
    )

    def setup_build_environment(self, env):
        env.set("MKL_ROOT", os.path.dirname(self.spec["intel-oneapi-mkl"].headers[0]))
