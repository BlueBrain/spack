# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Highfive(CMakePackage):
    """HighFive - Header only C++ HDF5 interface"""

    homepage = "https://github.com/BlueBrain/HighFive"
    url = "https://github.com/BlueBrain/HighFive/archive/v2.0.tar.gz"
    git = "https://github.com/BlueBrain/HighFive.git"

    version("master", branch="master")
    version("2.9.0", sha256="6301def8ceb9f4d7a595988612db288b448a3c0546f6c83417dab38c64994d7e")
    version("2.8.0", sha256="cd2502cae61bfb00e32dd18c9dc75289e09ad1db5c2a46d3b0eefd32e0df983b")
    version("2.7.1", sha256="25b4c51a94d1e670dc93b9b73f51e79b65d8ff49bcd6e5d5582d5ecd2789a249")
    version("2.7.0", sha256="8e05672ddf81a59ce014b1d065bd9a8c5034dbd91a5c2578e805ef880afa5907")
    version("2.6.2", sha256="ab51b9fbb49e877dd1aa7b53b4b26875f41e4e0b8ee0fc2f1d735e0d1e43d708")
    version("2.6.1", sha256="b5002c1221cf1821e02fb2ab891b0160bac88b43f56655bd844a472106ca3397")
    version("2.6.0", sha256="9f9828912619ba27d6f3a30e77c27669d9f19f6ee9170f79ee5f1ea96f85a4cd")
    version("2.5.1", sha256="1ba05aa31cdeda03d013094eebc10f932783e4e071e253e9eaa8889120f241c7")
    version("2.5.0", sha256="27f55596570df3cc8b878a1681a0d4ba0fe2e3da4a0ef8d436722990d77dc93a")
    version("2.4.1", sha256="6826471ef5c645ebf947d29574b302991525a8a8ff1ef687aba7311d9a0ea36f")
    version("2.4.0", sha256="ba0ed6d8e2e09e80849926f38c15a26cf4b80772084cea0555269a25fec02149")
    version("2.3.1", sha256="41728a1204bdfcdcef8cbc3ddffe5d744c5331434ce3dcef35614b831234fcd7")
    version("2.3", sha256="7da6815646eb4294f210cec6be24c9234d7d6ceb2bf92a01129fbba6583c5349")
    version("2.2.2", sha256="5bfb356705c6feb9d46a0507573028b289083ec4b4607a6f36187cb916f085a7")
    version("2.2.1", sha256="964c722ba916259209083564405ef9ce073b15e9412955fef9281576ea9c5b85")
    version("2.2", sha256="fe065f2443e38444100b43999a96916e81a0aa7e500cf768d3bf6f8392b8efee")
    version("2.1.1", sha256="52cffeda0d018f020f48e5460c051d5c2031c3a3c82133a21527f186a0c1650e")
    version("2.0", sha256="deee33d7f578e33dccb5d04771f4e01b89a980dd9a3ff449dd79156901ee8d25")
    version("1.5", sha256="f194bda482ab15efa7c577ecc4fb7ee519f6d4bf83470acdb3fb455c8accb407")
    version("1.2", sha256="4d8f84ee1002e8fd6269b62c21d6232aea3d56ce4171609e39eb0171589aab31")
    version("1.1", sha256="430fc312fc1961605ffadbfad82b9753a5e59482e9fbc64425fb2c184123d395")
    version("1.0", sha256="d867fe73d00817f686d286f3c69a23731c962c3e2496ca1657ea7302cd0bb944")

    # This is a header-only lib so dependencies shall be specified in the
    # target project directly and never specified here since they get truncated
    # when installed as external packages (which makes sense to improve reuse)
    variant("boost", default=False, description="Support Boost")
    variant("mpi", default=True, description="Support MPI")
    variant("eigen", default=False, description="Support Eigen")
    variant("xtensor", default=False, description="Support xtensor")
    variant(
        "page_buffer_patch",
        default=False,
        when="@2.6.2,2.7.1",
        description="Allow using the pagebuffer with pHDF5.",
    )

    # Develop builds tests which require boost
    conflicts("~boost", when="@develop")

    depends_on("boost @1.41: +serialization+system", when="+boost")

    depends_on("hdf5")
    depends_on("hdf5 ~mpi", when="~mpi")
    depends_on("hdf5 +mpi", when="+mpi")
    depends_on("hdf5 +mpi", when="+mpi~page_buffer_patch")

    # Using the page buffer with pHDF5 requires HDF5 to be patched. This
    # patch is currently only available for one version.
    depends_on("hdf5@1.12.1,1.14.0 +page_buffer_patch+mpi", when="+mpi+page_buffer_patch")

    depends_on("eigen", when="+eigen")
    depends_on("xtensor", when="+xtensor")
    depends_on("mpi", when="+mpi")

    # Enables the `PageBufferSize` property list also when building against pHDF5.
    patch(
        "remove-page-buffer-phdf5-check_v2.6.2.patch",
        when="@2.6.2+page_buffer_patch+mpi",
        sha256="7d9f63114902af0e5de9b4a1192e1de72ce384bdf401e7efbf434fb5f52d0ef7",
    )

    patch(
        "remove-page-buffer-phdf5-check_v2.7.1.patch",
        when="@2.7.1+page_buffer_patch+mpi",
        sha256="352074bc2fb30357425042878de2334ffc2e24ac8da9353fe8a7c9c6a62dd95f",
    )

    def cmake_args(self):
        return [
            "-DUSE_BOOST:Bool=" + str(self.spec.satisfies("+boost")),
            "-DUSE_EIGEN:Bool=" + str(self.spec.satisfies("+eigen")),
            "-DUSE_XTENSOR:Bool=" + str(self.spec.satisfies("+xtensor")),
            "-DHIGHFIVE_PARALLEL_HDF5:Bool=" + str(self.spec.satisfies("+mpi")),
            "-DHIGHFIVE_EXAMPLES:Bool=" + str(self.spec.satisfies("@develop")),
            "-DHIGHFIVE_UNIT_TESTS:Bool=" + str(self.spec.satisfies("@develop")),
            "-DHIGHFIVE_TEST_SINGLE_INCLUDES:Bool=" + str(self.spec.satisfies("@develop")),
            "-DHIGHFIVE_USE_INSTALL_DEPS:Bool=Off",
        ]
