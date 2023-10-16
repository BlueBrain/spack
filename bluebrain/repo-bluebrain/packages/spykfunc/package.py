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
    version("0.18.3", tag="v0.18.3")
    version("0.18.1", tag="v0.18.1")
    version("0.18.0", tag="v0.18.0")
    version("0.17.4", tag="v0.17.4")
    version("0.17.3", tag="v0.17.3")
    version("0.17.2", tag="v0.17.2")
    version("0.17.1", tag="v0.17.1")
    version("0.17.0", tag="v0.17.0")
    version("0.16.99", tag="v0.16.99")
    version("0.15.9", tag="v0.15.9")
    # versions 0.13.2-0.14.x require legacy mvdtool+python
    version("0.13.1", tag="v0.13.1")
    version("0.12.2", tag="v0.12.2")

    depends_on("cmake", type="build", when="@0.15.4:")
    depends_on("ninja", type="build", when="@0.17.3:")
    depends_on("boost", type=("build", "link"), when="@0.15.4:0.16.999")
    depends_on("morpho-kit", type=("build", "link"), when="@0.15.4:0.17.2")
    depends_on("random123", when="@0.17.0:0.17.2")

    depends_on("py-mvdtool~mpi", type=("build", "run"), when="@0.14.4:0.16.1")

    depends_on("python@3.6:")
    depends_on("py-cython", type="run", when="@:0.15.3")
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("spark+hadoop@3.0.0:", type="run")
    depends_on("hadoop@:2.999", type="run", when="@:0.17.1")
    depends_on("hadoop@3:", type="run", when="@0.17.2:")

    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-funcsigs", type=("build", "run"))
    depends_on("py-fz-td-recipe", type=("build", "run"), when="@0.17.3:")
    # h5py needed for morphologies before, and to supplement libSONATA due
    # to missing API functionality
    depends_on("py-h5py", type=("build", "run"), when="@:0.15.1,0.16.99:")
    depends_on("py-hdfs", type=("build", "run"))
    depends_on("py-jprops", type=("build", "run"))
    depends_on("py-libsonata@:0.1.14,0.1.17:", type="run", when="@0.15.3:")
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-morphio", type=("build", "run"), when="@0.17.2:")
    depends_on("py-morpho-kit", type=("build", "run"), when="@0.14.4:")
    depends_on("py-mpi4py", type=("build", "run"), when="@0.17.3:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"), when="@0.17.3:")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyarrow+parquet@3.0.0:", type=("build", "run"))
    depends_on("py-pyspark@3.0.0:", type=("build", "run"))

    # old dependencies
    depends_on("py-lazy-property", type=("build", "run"), when="@:0.16")
    depends_on("py-progress", type=("build", "run"), when="@:0.16")
    depends_on("py-six", type=("build", "run"), when="@0.15.7:0.16")
    depends_on("py-sparkmanager", type=("build", "run"), when="@:0.15.6")

    patch("setup-spark3.patch", when="@:0.15.6 ^spark@3:")
    patch("properties-spark3.patch", when="@:0.15.6 ^spark@3:")
    patch("bogus-h5py.patch", when="@0.15.2:0.15.9")

    def patch(self):
        if self.spec.satisfies("@:0.16.1"):
            filter_file("srun", "srun --mpi=none", "scripts/sm_cluster")

    def setup_build_environment(self, env):
        # This is a rather ugly setup to run spykfunc without having to
        # activate all python packages.
        env.set("BOOST_ROOT", self.spec["boost"].prefix)

    def setup_run_environment(self, env):
        env.set("SPARK_HOME", self.spec["spark"].prefix)
        env.set("HADOOP_HOME", self.spec["hadoop"].prefix)
