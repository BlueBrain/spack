from spack.package import *
from spack.pkg.builtin.py_numpy import PyNumpy as BuiltinPyNumpy


class PyNumpy(BuiltinPyNumpy):
    __doc__ = BuiltinPyNumpy.__doc__

    version("1.23.5", sha256="1b1766d6f397c18153d40015ddfc79ddb715cabadc04d2d228d4e5a8bc4ded1a")
