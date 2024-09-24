##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ParquetConverters(CMakePackage):
    """Parquet conversion tools developed by Blue Brain Project, EPFL"""

    homepage = "https://github.com/BlueBrain/parquet-converters"
    git = "https://github.com/BlueBrain/parquet-converters.git"

    submodules = True

    version("develop", branch="main")
    version("0.9.0", tag="v0.9.0")

    depends_on("mpi")

    depends_on("arrow+parquet+snappy@3.0.0:")
    depends_on("catch2", type="build")
    depends_on("hdf5+mpi")
    depends_on("highfive+mpi", type="build")
    depends_on("nlohmann-json", type="build")
    depends_on("range-v3@0.11:", type="build")

    def cmake_args(self):
        return [
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
        ]
