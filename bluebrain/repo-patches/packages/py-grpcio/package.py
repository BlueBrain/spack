from spack.package import *
from spack.pkg.builtin.py_grpcio import PyGrpcio as BuiltinPyGrpcio


class PyGrpcio(BuiltinPyGrpcio):
    __doc__ = BuiltinPyGrpcio.__doc__

    version("1.51.1", sha256="e6dfc2b6567b1c261739b43d9c59d201c1b89e017afd9e684d85aa7a186c9f7a")

    depends_on("python@3.7:", when="@1.51:", type=("build", "link", "run"))
