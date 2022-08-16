from spack import *
from spack.pkg.builtin.ipopt import Ipopt as BuiltinIpopt


class Ipopt(BuiltinIpopt):
    __doc__ = BuiltinIpopt.__doc__

    url = "https://github.com/coin-or/Ipopt/archive/releases/3.13.2.tar.gz"

    variant('thirdparty-hsl', default=False,
            description="Build with Thirdparty Coin Harwell Subroutine Libraries shim")

    depends_on('thirdparty-hsl', when='+thirdparty-hsl')

    # Can't depend on both HSL ways at once
    conflicts('+coinhsl', when='+thirdparty-hsl')

    def configure_args(self):
        spec = self.spec

        args = super().configure_args()

        if 'thirdparty-hsl' in spec:
            args.extend([
                '--with-hsl-lib=%s' % spec['thirdparty-hsl'].libs.ld_flags,
                '--with-hsl-incdir=%s' % spec['thirdparty-hsl'].prefix.include])

        return args
