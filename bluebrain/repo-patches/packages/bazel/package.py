from spack import *
from spack.pkg.builtin.bazel import Bazel as BuiltinBazel


class Bazel(BuiltinBazel):
    __doc__ = BuiltinBazel.__doc__

    version('4.2.2', sha256='9981d0d53a356c4e87962847750a97c9e8054e460854748006c80f0d7e2b2d33')

    patch('https://github.com/bazelbuild/bazel/commit/9761509f9ccc3892f42425b904adf1ef10bcb1f4.patch',
          sha256='663f4c1145b53518500a205f644d06cd2b70cdf5a630c9ab77d8a363fb07e8e6')
    patch('https://github.com/bazelbuild/bazel/commit/8cc0e261a313dbf5e81bfeca2bafa3e12a991046.patch',
          sha256='fb1c25be40c26f7cb01770a8c31e3e6d24bfa03feff8fe0eedad5ed87c8b94fd')
