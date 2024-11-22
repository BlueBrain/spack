##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Appositionizer(CMakePackage):
    """Detects appositions between cells"""

    homepage = "https://github.com/BlueBrain/appositionizer"
    git = "https://github.com/BlueBrain/appositionizer.git"

    generator("ninja")
    submodules = True

    version("develop", branch="main")
    version("1.0.0", tag="v1.0.0")

    variant("caliper", default=True, description="Enables profiling with Caliper")
    variant("test", default=False, description="Enables building tests")

    depends_on("cmake", type="build")
    depends_on("ninja", type="build")

    depends_on("mpi")

    depends_on("caliper@2.8.0:+mpi", when="+caliper")
    depends_on("catch2@3")
    depends_on("eigen")
    depends_on("fmt cxxstd=20")
    depends_on("intel-oneapi-tbb")
    depends_on("libsonata@0.1.9: cxxstd=20")
    depends_on("morphio@3.3.5:")
    depends_on("nlohmann-json")
    depends_on("random123")
    depends_on("range-v3@:0.10")
    depends_on("yaml-cpp")

    depends_on("highfive+mpi")

    def cmake_args(self):
        use_tests = self.spec.satisfies("@develop") or "+test" in self.spec
        args = [
            self.define_from_variant("ENABLE_CALIPER", "caliper"),
            self.define("ENABLE_TESTS", use_tests),
        ]
        return args
