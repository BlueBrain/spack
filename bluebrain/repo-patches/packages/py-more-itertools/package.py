from spack.package import *
from spack.pkg.builtin.py_more_itertools import (
    PyMoreItertools as BuiltinPyMoreItertools,
)


class PyMoreItertools(BuiltinPyMoreItertools):
    __doc__ = BuiltinPyMoreItertools.__doc__

    version('8.11.0', sha256='0a2fd25d343c08d7e7212071820e7e7ea2f41d8fb45d6bc8a00cd6ce3b7aab88')
