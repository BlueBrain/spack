# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Neuron(CMakePackage):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments. The primary scripting
    language is hoc but a Python interface is also available.
    """

    homepage = "https://www.neuron.yale.edu/"
    url = "https://github.com/neuronsimulator/nrn/releases/download/8.2.3/nrn-full-src-package-8.2.3.tar.gz"
    git = "https://github.com/neuronsimulator/nrn"
    maintainers("pramodk", "nrnhines", "iomaganaris", "ohm314", "matz-e")

    version("develop", branch="master")
    # TODO: for testing purposes, remove it
    version("9.0", commit="53c9392d7")
    version("9.0.a14", commit="bd9426d9")
    version("8.2.3", tag="8.2.3")
    version("8.2.0", tag="8.2.0")
    version("8.1.0", tag="8.1.0")
    version("8.0.0", tag="8.0.0")
    version("7.8.2", tag="7.8.2")

    # neuron variants for basic installation
    variant("interviews", default=False, description="Enable GUI with INTERVIEWS")
    variant("legacy-unit", default=False, description="Enable legacy units")
    variant("mpi", default=True, description="Enable MPI parallelism")
    variant("python", default=True, description="Enable python")
    variant("tests", default=False, description="Enable building tests")
    variant("rx3d", default=False, description="Enable cython translated 3-d rxd.", when="+python")

    # variants from coreneuron support
    variant("coreneuron", default=True, description="Enable CoreNEURON support")
    variant("gpu", default=False, description="Enable GPU build", when="@9:+coreneuron")
    variant("openmp", default=False, description="Enable CoreNEURON OpenMP support", when="+coreneuron")

    # instrumentation for performance measurement
    variant("caliper", default=False, description="Add Caliper support")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "FastDebug", "RelWithDebInfo", "Release"),
    )

    # extended set of model tests
    variant(
        "model_tests",
        default="None",
        description="Enable detailed model tests included in neuron",
        multi=True,
        values=("None", "olfactory", "channel-benchmark", "tqperf-heavy"),
    )

    # Build with `ninja` instead of `make`
    generator = "Ninja"

    # common build dependencies
    depends_on("bison@3:", type="build")
    depends_on("flex@2.6:", type="build")
    depends_on("ninja", type="build")

    # build and link dependencies
    depends_on("gettext")
    depends_on("mpi", when="+mpi")
    depends_on("ncurses")
    depends_on("readline")

    # dependencies from python variants
    depends_on("python", when="+python")
    depends_on("py-pytest", when="+python+tests")
    depends_on("py-mpi4py", when="+mpi+python+tests")
    depends_on("py-numpy", when="+python")
    depends_on("py-cython", when="+rx3d", type="build")
    depends_on("py-pytest-cov", when="+tests")
    # next two needed after neuronsimulator/nrn#2235.
    depends_on("py-pip", type=("build"), when="@9:")
    depends_on("py-packaging", type=("run"), when="@9:")

    # dependencies from coreneuron
    depends_on("boost", when="+coreneuron+tests")
    depends_on("cuda", when="+coreneuron+gpu")
    depends_on("py-sympy@1.3:", when="+coreneuron")

    # dependencies for performance measurement
    depends_on("caliper", when="+caliper")

    gpu_compiler_message = "neuron: for gpu build use %nvhpc"
    conflicts("%gcc", when="+gpu", msg=gpu_compiler_message)
    conflicts("%intel", when="+gpu", msg=gpu_compiler_message)

    patch("patch-v782-git-cmake-avx512.patch", when="@7.8.2")

    def cmake_args(self):
        spec = self.spec

        def cmake_options(spec_options):
            value = "TRUE" if spec_options in spec else "FALSE"
            cmake_name = spec_options[1:].upper().replace("-", "_")
            return "-DNRN_ENABLE_" + cmake_name + ":BOOL=" + value

        args = [
            cmake_options(variant)
            for variant in [
                "+coreneuron",
                "+interviews",
                "+mpi",
                "+python",
                "+rx3d",
                "+tests",
            ]
        ]

        if spec.satisfies("@:8"):
            args.append("-DNRN_ENABLE_BINARY_SPECIAL=ON")

        # dynamic mpi support not possible in case of gpu support
        if "+mpi" in spec:
            dynamic_mpi = "OFF" if "+gpu" in spec else "ON"
            args.append("-DNRN_ENABLE_MPI_DYNAMIC=%s" % dynamic_mpi)

        if "+python" in spec:
            args.append("-DPYTHON_EXECUTABLE:FILEPATH=" + spec["python"].command.path)

        if "+legacy-unit" in spec:
            args.append("-DNRN_DYNAMIC_UNITS_USE_LEGACY=ON")

        if "+caliper" in spec:
            args.append("-DNRN_ENABLE_PROFILING=ON")
            args.append("-DNRN_PROFILER=caliper")
            args.append("-DCORENRN_ENABLE_CALIPER_PROFILING=ON")

        # cmake options for coreneuron
        if spec.satisfies("+coreneuron"):
            options = [
                "-DCORENRN_ENABLE_SPLAYTREE_QUEUING=ON",
                "-DCORENRN_ENABLE_TIMEOUT=OFF",
                "-DCORENRN_ENABLE_OPENMP=%s" % ("ON" if "+openmp" in spec else "OFF"),
                "-DCORENRN_ENABLE_LEGACY_UNITS=%s" % ("ON" if "+legacy-unit" in spec else "OFF"),
                "-DCORENRN_ENABLE_UNIT_TESTS=%s" % ("ON" if "+tests" in spec else "OFF"),
            ]

            nmodl_options = "codegen --force"
            options.append("-DCORENRN_NMODL_FLAGS=%s" % nmodl_options)

            if spec.satisfies("+gpu"):
                nvcc = which("nvcc")
                options.append(self.define("CMAKE_CUDA_COMPILER", nvcc))
                options.append(self.define("CORENRN_ENABLE_GPU", True))

            args.extend(options)

        # cache performance for build neuronsimulator/nrn/pull/1574
        if spec.satisfies("@8.2:"):
            args.append("-DNRN_AVOID_ABSOLUTE_PATHS=ON")

        # enable tests that are selected via variant
        if spec.variants["model_tests"].value != ("None",):
            args.append(
                "-DNRN_ENABLE_MODEL_TESTS="
                + ",".join(model for model in spec.variants["model_tests"].value)
            )

        if spec.variants["build_type"].value in ["Release", "RelWithDebInfo"]:
            args.append("-DNRN_ENABLE_MATH_OPT=ON")

        if spec.satisfies("+gpu"):
            # Instead of assuming that the gcc in $PATH is the right host compiler, take the
            # compiler used to build the cuda package as the CUDA host compiler.
            host_compiler_spec = spec["cuda"].compiler
            # Surely this isn't the best way
            host_compiler_candidates = [
                c for c in spack.compilers.all_compilers() if c.spec == host_compiler_spec
            ]
            assert len(host_compiler_candidates) == 1
            host_compiler = host_compiler_candidates[0]
            options.append(self.define("CMAKE_CUDA_HOST_COMPILER", host_compiler.cxx))
            args.extend(options)

        return args

    @run_after("install")
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        spec = self.spec

        if "cray" in spec.architecture:
            cc_compiler = "cc"
            cxx_compiler = "CC"
        elif spec.satisfies("+mpi"):
            cc_compiler = spec["mpi"].mpicc
            cxx_compiler = spec["mpi"].mpicxx
        else:
            cc_compiler = self.compiler.cc
            cxx_compiler = self.compiler.cxx

        kwargs = {"backup": False, "string": True}
        nrnmech_makefile = join_path(self.prefix, "bin/nrnmech_makefile")

        # assign_operator is changed to fix wheel support
        if spec.satisfies("@:7.99"):
            assign_operator = "?="
        else:
            assign_operator = "="

        filter_file(
            "CC {0} {1}".format(assign_operator, env["CC"]),
            "CC = {0}".format(cc_compiler),
            nrnmech_makefile,
            **kwargs,
        )

        filter_file(
            "CXX {0} {1}".format(assign_operator, env["CXX"]),
            "CXX = {0}".format(cxx_compiler),
            nrnmech_makefile,
            **kwargs,
        )

        # for coreneuron
        if spec.satisfies("@9:+coreneuron"):
            nrnmakefile = join_path(self.prefix, "share/coreneuron/nrnivmodl_core_makefile")
            filter_file(env["CXX"], self.compiler.cxx, nrnmakefile, **kwargs)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
        if spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", spec.prefix.lib.python)
