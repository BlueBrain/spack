from spack import *
from spack.pkg.builtin.arm_forge import ArmForge as BuiltinArmForge


class ArmForge(BuiltinArmForge):
    __doc__ = BuiltinArmForge.__doc__

    version(
        "22.0.1-Linux-x86_64",
        sha256="8f8a61c159665d3de3bc5334ed97bdb4966bfbdb91b65d32d162d489eb2219ac",
        url="https://content.allinea.com/downloads/arm-forge-22.0.1-linux-x86_64.tar",
    )

    version(
        "20.2.0-Redhat-7.0-x86_64",
        sha256="26592a77c42f970f724f15b70cc5ce6af1078fd0ef9243a37c3215916cfa7cf4",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-7.0-x86_64.tar",
    )
