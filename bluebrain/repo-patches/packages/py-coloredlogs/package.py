from spack import *
from spack.pkg.builtin.py_coloredlogs import \
    PyColoredlogs as BuiltinPyColoredlogs


class PyColoredlogs(BuiltinPyColoredlogs):
    __doc__ = BuiltinPyColoredlogs.__doc__

    version('15.0', sha256='5e78691e2673a8e294499e1832bb13efcfb44a86b92e18109fa18951093218ab')
