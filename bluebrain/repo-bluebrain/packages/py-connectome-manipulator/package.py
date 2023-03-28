# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyConnectomeManipulator(PythonPackage):
    """Connectome generator tool."""

    homepage = "https://bbpgitlab.epfl.ch/conn/structural/connectome_manipulator"
    git = "git@bbpgitlab.epfl.ch:conn/structural/connectome_manipulator.git"

    version("develop", branch="main")
    version("0.0.3", tag="connectome-manipulator-v0.0.3")

    depends_on("parquet-converters@0.8.0:", type="run")

    depends_on("py-bluepysnap@1.0.5:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-progressbar", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-submitit", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))
    depends_on("py-pyarrow", type=("build", "run"))
    depends_on("py-jsonpickle", type=("build", "run"))
    depends_on("py-submitit", type=("build", "run"))

    def setup_run_environment(self, env):
        """Add parquet-converters to the PATH."""
        env.prepend_path("PATH", os.path.join(self.spec["parquet-converters"].prefix, "bin"))
