from spack.package import *
from spack.pkg.builtin.llvm import Llvm as BuiltinLlvm


class Llvm(BuiltinLlvm):
    __doc__ = BuiltinLlvm.__doc__
    # We need a modern linker to use modern compilers
    depends_on("binutils+ld", type="run")
    # LLVM's libomp.so doesn't have an rpath for libhwloc.so
    depends_on("hwloc", type="run")
