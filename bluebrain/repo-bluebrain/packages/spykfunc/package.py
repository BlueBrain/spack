##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Spykfunc(PythonPackage):
    """Spykfunc - Spark functionalizer developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/circuit-building/spykfunc"
    url = "ssh://git@bbpgitlab.epfl.ch/hpc/circuit-building/spykfunc.git"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/circuit-building/spykfunc.git"

    submodules = True

    version("develop", branch="main")
    version("0.18.5", tag="v0.18.5")

    depends_on("cmake", type="build")
    depends_on("ninja", type="build")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    depends_on("spark+hadoop@3.0.0:", type="run")
    depends_on("hadoop@3:", type="run")

    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-fz-td-recipe", type=("build", "run"))
    # h5py needed for morphologies before, and to supplement libSONATA due
    # to missing API functionality
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-hdfs", type=("build", "run"))
    depends_on("py-jprops", type=("build", "run"))
    depends_on("py-libsonata@0.1.17:", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-morphio", type=("build", "run"))
    depends_on("py-morpho-kit", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyarrow+dataset+parquet@3.0.0:", type=("build", "run"))
    depends_on("py-pyspark@3.0.0:", type=("build", "run"))

    def setup_run_environment(self, env):
        env.set("SPARK_HOME", self.spec["spark"].prefix)
        env.set("HADOOP_HOME", self.spec["hadoop"].prefix)
