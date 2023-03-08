from spack.package import *
from spack.pkg.builtin.llvm import Llvm as BuiltinLlvm


class Llvm(BuiltinLlvm):
    __doc__ = BuiltinLlvm.__doc__
    # We need a modern linker to use modern compilers
    depends_on("binutils+ld", type="run")
