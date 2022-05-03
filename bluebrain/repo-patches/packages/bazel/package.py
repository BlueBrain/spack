from spack import *
from spack.pkg.builtin.bazel import Bazel as BuiltinBazel


class Bazel(BuiltinBazel):
    __doc__ = BuiltinBazel.__doc__

    version('5.1.1', sha256='7f5d3bc1d344692b2400f3765fd4b5c0b636eb4e7a8a7b17923095c7b56a4f78')
