##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyFunctionalizer(PythonPackage):
    """Functionalizer - Spark functionalizer developed by Blue Brain Project, EPFL"""

    homepage = "https://github.com/BlueBrain/functionalizer"
    pypi = "functionalizer/functionalizer-1.0.0.tar.gz"

    version("1.0.0", sha256="c62754fcf41e29729386c23cefb0dd57b449ac27c0b47ba5e2e4b2776c517494")

    depends_on("py-cmake", type="build")
    depends_on("py-ninja", type="build")
    depends_on("py-scikit-build-core+pyproject", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("spark+hadoop@3.0.0:", type="run")
    depends_on("hadoop@3:", type="run")

    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-fz-td-recipe@0.2:", type=("build", "run"))
    # h5py needed for morphologies before, and to supplement libSONATA due
    # to missing API functionality
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-hdfs", type=("build", "run"))
    depends_on("py-jprops", type=("build", "run"))
    depends_on("py-libsonata@0.1.17:", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-morphio", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyarrow+dataset+parquet@3.0.0:", type=("build", "run"))
    depends_on("py-pyspark@3.0.0:", type=("build", "run"))

    def setup_run_environment(self, env):
        env.set("SPARK_HOME", self.spec["spark"].prefix)
        env.set("HADOOP_HOME", self.spec["hadoop"].prefix)
