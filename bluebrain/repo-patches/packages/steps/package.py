# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Steps(CMakePackage):
    """STochastic Engine for Pathway Simulation"""

    homepage = "https://groups.oist.jp/cnu/software"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/HBP_STEPS.git"

    maintainers("tristan0x")

    submodules = True

    version("develop", branch="master")
    version("5.0.2", tag="5.0.2")
    version("5.0.1", tag="5.0.1")
    version("4.1.0", tag="4.1.0")

    variant(
        "codechecks",
        default=False,
        description="Perform additional code checks like code formatting or static analysis",
    )
    variant(
        "native",
        default=False if sys.platform == "darwin" else True,
        description="Generate non-portable arch-specific code",
    )
    variant("blender", default=False, description="Build stepsblender package")
    variant("lapack", default=False, description="Use new BDSystem/Lapack code for E-Field solver")
    variant("distmesh", default=True, description="Add solvers based on distributed mesh")
    variant("petsc", default=True, description="Use PETSc library for parallel E-Field solver")
    variant("mpi", default=True, description="Use MPI for parallel solvers")
    variant("bundle", default=False, description="Use bundled libraries")
    variant("stochtests", default=True, description="Add stochastic tests to ctests")
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "RelWithDebInfoAndAssert"),
    )
    variant(
        "caliper", default=False, description="Build in caliper support (Instrumentor Interface)"
    )
    variant(
        "likwid", default=False, description="Build in likwid support (Instrumentor Interface)"
    )
    variant("vesicle", default=True, when="@5:", description="Add vesicle model")

    # Build with `Ninja` instead of `Unix Makefiles`
    generator("ninja")

    conflicts("+distmesh~mpi", msg="steps+distmesh requires +mpi")
    depends_on("benchmark", type=("build", "test"))
    depends_on("blas")
    depends_on("boost", type="build")
    depends_on("caliper", when="+caliper")
    depends_on("easyloggingpp", when="~bundle")
    depends_on("eigen")
    depends_on("gmsh", when="+distmesh")
    depends_on("gsl", when="@:5.0.1+vesicle")
    depends_on("lapack", when="+lapack")
    depends_on("likwid", when="+likwid")
    depends_on("metis+int64")
    depends_on("mpi", when="+mpi")
    depends_on("ninja", type="build")
    depends_on("omega-h+gmsh+mpi", when="~bundle+distmesh")
    depends_on("petsc~debug+int64+mpi", when="+petsc+mpi")
    depends_on("petsc~debug+int64~mpi", when="+petsc~mpi")
    depends_on("pkgconfig", type="build")
    depends_on("py-cython")
    depends_on("py-h5py", type=("build", "test", "run"))
    depends_on("py-pip", type="build", when="@5:")
    depends_on("py-matplotlib", type=("build", "test"))
    depends_on("py-build", type="build", when="@5:")
    depends_on("py-mpi4py", when="+distmesh", type=("build", "test", "run"))
    depends_on("py-numpy", type=("build", "test", "run"))
    depends_on("py-scipy", type=("build", "test", "run"))
    depends_on("python", type=("build", "test", "run"))
    depends_on("random123", when="~bundle")
    depends_on("sundials@:2+int64", when="@:5~bundle")
    depends_on("sundials@:6+int64", when="@develop~bundle")

    patch("for_aarch64.patch", when="@:4 target=aarch64:")

    def patch(self):
        # easylogging is a terrible library that requires compilation by
        # its dependents: splice in disabling all errors
        filter_file(r"(-Wno-double-promotion)", r"-Wno-error \1", "src/steps/util/CMakeLists.txt")
        # unittest2 is unmaintained, shan't be used and does not build with modern Python
        filter_file("unittest2", "", "requirements.txt", ignore_absent=True)

    def cmake_args(self):
        python_interpreter = self.spec["python"].prefix.bin.python + str(
            self.spec["python"].version.up_to(1)
        )
        args = [
            self.define("STEPS_INSTALL_PYTHON_DEPS", False),
            self.define_from_variant("BUILD_STOCHASTIC_TESTS", "stochtests"),
            self.define_from_variant("BUILD_TESTING", "codechecks"),
            self.define_from_variant("STEPS_ENABLE_ERROR_ON_WARNING", "codechecks"),
            self.define_from_variant("STEPS_TEST_FORMATTING", "codechecks"),
            self.define_from_variant("STEPS_USE_CALIPER_PROFILING", "caliper"),
            self.define_from_variant("STEPS_USE_DIST_MESH", "distmesh"),
            self.define_from_variant("STEPS_USE_LIKWID_PROFILING", "likwid"),
            self.define_from_variant("STEPS_USE_STEPSBLENDER", "blender"),
            self.define_from_variant("STEPS_USE_VESICLE_SOLVER", "vesicle"),
            self.define_from_variant("TARGET_NATIVE_ARCH", "native"),
            self.define_from_variant("USE_BDSYSTEM_LAPACK", "lapack"),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("USE_PETSC", "petsc"),
            "-DBLAS_LIBRARIES=" + self.spec["blas"].libs.joined(";"),
            f"-DPYTHON_EXECUTABLE={python_interpreter}",
        ]

        args.extend(
            [
                self.define_from_variant(f"USE_BUNDLE_{bundle}", "bundle")
                for bundle in ["EASYLOGGINGPP", "OMEGA_H", "RANDOM123", "SUNDIALS", "SUPERLU_DIST"]
            ]
        )

        return args

    def setup_run_environment(self, env):
        # This recipe exposes a Python package from a C++ CMake project.
        # This hook is required to reproduce what Spack PythonPackage does.
        env.prepend_path("PYTHONPATH", self.prefix)
