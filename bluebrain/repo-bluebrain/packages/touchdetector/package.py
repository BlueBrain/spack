##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Touchdetector(CMakePackage):
    """Detects touches between cells
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/touchdetector"
    url = "ssh://git@bbpgitlab.epfl.ch/hpc/touchdetector.git"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/touchdetector.git"

    generator = "Ninja"
    submodules = True

    version('develop', branch='main')
    version('5.7.0', tag='5.7.0')
    version('5.6.1', tag='5.6.1')
    version('5.6.0', tag='5.6.0')
    version('5.5.1', tag='5.5.1')
    version('5.5.0', tag='5.5.0')
    version('5.4.0', tag='5.4.0')
    version('5.3.4', tag='5.3.4')
    version('5.3.3', tag='5.3.3')
    version('5.3.2', tag='5.3.2')
    version('5.3.1', tag='5.3.1')
    version('5.3.0', tag='5.3.0')
    version('5.2.0', tag='5.2.0')
    version('5.1.0', tag='5.1.0')
    version('5.0.1', tag='5.0.1')
    version('5.0.0', tag='5.0.0')
    version('4.4.2', tag='4.4.2')
    version('4.4.1', tag='4.4.1')
    version('4.3.3', tag='4.3.3')

    variant('openmp', default=False, description='Enables OpenMP support')
    variant('caliper', default=True, description='Enables profiling with Caliper')
    variant('asan', default=False, description='Enables AdressSanitizer')
    variant('ubsan', default=False, description='Enables UndefinedBehaviourSanitizer')
    variant('clang-tidy', default=False, description='Enables static analysis with clang-tidy')
    variant('test', default=False, description='Enables building tests')
    variant('benchmark', default=False, description='Enables benchmarks')

    depends_on('cmake', type='build')
    depends_on('ninja', type='build')
    depends_on('catch2@2', when='@5.0.2:')
    depends_on('eigen', when='@4.5:')
    depends_on('fmt@:5.999', when='@4.5:')
    depends_on('morpho-kit', when='@5.2:')
    depends_on('mpi')
    depends_on('pugixml', when='@4.5:')
    depends_on('random123', when='@5.3.3:')
    depends_on('range-v3@:0.4', when='@5.0.2:5.3.2')
    depends_on('range-v3@:0.10', when='@5.3.3:')
    depends_on('libsonata@0.1.9:', when='@5.6.0:')
    depends_on('nlohmann-json', when='@5.3.3:')
    depends_on('intel-oneapi-tbb', when='@5.7.0:')
    depends_on('caliper@2.8.0:+mpi', when='+caliper@5.7.0:')
    depends_on('benchmark', when='+benchmark@5.7.0:')

    depends_on('mvapich2', when='+asan@5.7.0:')
    depends_on('mvapich2', when='+ubsan@5.7.0:')

    # Boost 1.79.0 deprecated and broke the includes related to `fs::ofstream`
    # which is used by TD. See,
    #    https://www.boost.org/users/history/version_1_79_0.html
    conflicts('boost@1.79.0', when='@:5.6.1')

    # Old dependencies
    depends_on('hpctools~openmp', when='~openmp@:4.4')
    depends_on('hpctools+openmp', when='+openmp@:4.4')
    depends_on('libxml2', when='@:4.4')
    depends_on('zlib', when='@:4.4')

    depends_on('morphio@2.0.8:', when='@4.5:5.1')
    depends_on('mvdtool@2.1.0:', when='@5.1.1:5.5.999')
    depends_on('mvdtool@1.5.1:2.0.0', when='@4.5:5.1')

    depends_on('highfive+mpi', when='@5.3.0:5.6.1')
    depends_on('boost@1.50:', when='@:5.6.1')

    patch("no-wall.patch", when='@5:5.4.999')
    patch("fix-cmake.patch", when='@5.6.1')

    def patch(self):
        if self.spec.satisfies('@5.6.1'):
            filter_file(r'(int messageLength) = -1;$',
                        r'\1 = 0;',
                        'touchdetector/DistributedTouchDetector.cxx')

    def cmake_args(self):
        args = [
            self.define_from_variant('USE_OPENMP', 'openmp'),
        ]

        if self.spec.satisfies('@:5.6.1'):
            args += [
                self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc),
                self.define('CMAKE_CXX_COMPILER', self.spec['mpi'].mpicxx),
            ]

        if self.spec.satisfies('@5.7.0'):
            use_tests = self.spec.satisfies('@develop') or '+test' in self.spec
            args += [
                self.define_from_variant('ENABLE_CALIPER', 'caliper'),
                self.define_from_variant('ENABLE_ASAN', 'asan'),
                self.define_from_variant('ENABLE_UBSAN', 'ubsan'),
                self.define_from_variant('ENABLE_BENCHMARKS', 'benchmark'),
                self.define('ENABLE_TESTS', use_tests),
            ]

            if '+clang-tidy' in self.spec:
                self.args.append(
                    self.define('CMAKE_CXX_CLANG_TIDY', 'clang-tidy'),
                )

        return args

    def setup_build_environment(self, env):
        # The default CMAKE_PREFIX_PATH may not contain the necessary symlink to the TBB
        # CMake glue, set it ourselves.
        #
        # This conditional needs to be removed in 2023 with a new deployment.
        if hasattr(self.spec["tbb"].package, "component_prefix"):
            env.prepend_path("CMAKE_PREFIX_PATH", self.spec["tbb"].package.component_prefix)
