##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Touchdetector(CMakePackage):
    """Detects touches between cells"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/touchdetector"
    url = "ssh://git@bbpgitlab.epfl.ch/hpc/touchdetector.git"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/touchdetector.git"

    generator("ninja")
    submodules = True

    version("develop", branch="main")
    version("7.0.0", tag="v7.0.0")
    version("6.0.3", tag="6.0.3")

    variant("caliper", default=True, description="Enables profiling with Caliper")
    variant("asan", default=False, description="Enables AdressSanitizer")
    variant("ubsan", default=False, description="Enables UndefinedBehaviourSanitizer")
    variant("clang-tidy", default=False, description="Enables static analysis with clang-tidy")
    variant("test", default=False, description="Enables building tests")
    variant("benchmark", default=False, description="Enables benchmarks")

    depends_on("cmake", type="build")
    depends_on("ninja", type="build")

    depends_on("mpi")

    depends_on("benchmark", when="+benchmark")
    depends_on("caliper@2.8.0:+mpi", when="+caliper")
    depends_on("catch2@2", when="@6")
    depends_on("catch2@3", when="@7:")
    depends_on("eigen")
    depends_on("fmt@:5.999 cxxstd=20")
    depends_on("intel-oneapi-tbb")
    depends_on("libsonata@0.1.9: cxxstd=20")
    depends_on("morphio@3.3.5:", when="@7:")
    depends_on("morpho-kit@0.3.5:", when="@:6.0.3")
    depends_on("nlohmann-json")
    depends_on("pugixml", when="@4.5:6")
    depends_on("random123", when="@5.3.3:")
    depends_on("range-v3@:0.10", when="@5.3.3:")
    depends_on("yaml-cpp", when="@7:")

    depends_on("mvapich2", when="+asan@5.7.0:")
    depends_on("mvapich2", when="+ubsan@5.7.0:")

    depends_on("highfive+mpi", when="@7:")

    def patch(self):
        if self.spec.satisfies("@5.6.1"):
            filter_file(
                r"(int messageLength) = -1;$",
                r"\1 = 0;",
                "touchdetector/DistributedTouchDetector.cxx",
            )

    def cmake_args(self):
        args = []

        if self.spec.satisfies("@:5.6.1"):
            args += [
                self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
                self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
            ]

        if self.spec.satisfies("@5.7.0:"):
            use_tests = self.spec.satisfies("@develop") or "+test" in self.spec
            args += [
                self.define_from_variant("ENABLE_CALIPER", "caliper"),
                self.define_from_variant("ENABLE_ASAN", "asan"),
                self.define_from_variant("ENABLE_UBSAN", "ubsan"),
                self.define_from_variant("ENABLE_BENCHMARKS", "benchmark"),
                self.define("ENABLE_TESTS", use_tests),
            ]

            if "+clang-tidy" in self.spec:
                self.args.append(self.define("CMAKE_CXX_CLANG_TIDY", "clang-tidy"))

        return args

    def setup_build_environment(self, env):
        # The default CMAKE_PREFIX_PATH may not contain the necessary symlink to the TBB
        # CMake glue, set it ourselves.
        #
        # This conditional needs to be removed in 2023 with a new deployment.
        if "tbb" in self.spec and hasattr(self.spec["tbb"].package, "component_prefix"):
            env.prepend_path("CMAKE_PREFIX_PATH", self.spec["tbb"].package.component_prefix)
