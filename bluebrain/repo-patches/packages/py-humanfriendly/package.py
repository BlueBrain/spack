from spack import *
from spack.pkg.builtin.py_humanfriendly import \
    PyHumanfriendly as BuiltinPyHumanfriendly


class PyHumanfriendly(BuiltinPyHumanfriendly):
    __doc__ = BuiltinPyHumanfriendly.__doc__

    version('9.1', sha256='066562956639ab21ff2676d1fda0b5987e985c534fc76700a19bd54bcb81121d')
