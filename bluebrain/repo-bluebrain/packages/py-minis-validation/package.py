# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMinisValidation(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://github.com/BlueBrain/minis-validation"
    git = "https://github.com/BlueBrain/minis-validation.git"

    version("0.0.5.2024-10-11", commit="fdcb9e60fbab8239f98e2cc699348c1fdb83a550")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.14:1", type=("build", "run"))
    depends_on("py-pandas@2.0.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.1.1:", type=("build", "run"))
    depends_on("py-h5py@3.0:3", type=("build", "run"))
    depends_on("py-click@8.1.3:", type=("build", "run"))
    depends_on("py-tqdm@4.64.1", type=("build", "run"))
    depends_on("py-submitit@1.4.5:1", type=("build", "run"))
    depends_on("py-pyyaml@6.0:", type=("build", "run"))
    depends_on("py-types-pyyaml@6.0.12.10:", type=("build", "run"))
    depends_on("py-bluepysnap@3:", type=("build", "run"))
    depends_on("py-bluecellulab@2:", type=("build", "run"))

    def patch(self):
        # Purge version constraints caused by old (outdated) numba incompatibilities
        filter_file(r'((dask|distributed).*),<=.*([\'"])', r"\1\3", "setup.py")

    def setup_run_environment(self, env):
        env.set("NEURON_INIT_MPI", "0")
        env.unset("PMI_RANK")
