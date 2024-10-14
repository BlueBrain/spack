# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluecellulab(PythonPackage):
    """Pythonic Blue Brain simulator access, former BGLibPy"""

    homepage = "https://github.com/BlueBrain/BlueCelluLab"
    pypi = "bluecellulab/bluecellulab-1.7.6.tar.gz"

    version("2.6.15", sha256="8e366debbd0b531826d49264b8349a0f18d3741f3cd71cf0b8a14a3569a69a19")
    version("2.6.11", sha256="00bedd9d57f0c484a44ddc424d5c49d4c57d16691b4d7a40da6699bc4983966d")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    depends_on("neuron+python@8:", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-matplotlib@3.0.0:", type=("build", "run"))

    depends_on("py-bluepysnap@3:", type=("build", "run"))

    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-pydantic@2:", type=("build", "run"))
    depends_on("py-typing-extensions@4.8.0", type="run")

    depends_on("py-libsonata@0.1.26:")
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))

    # skip import test, because bluecellulab needs HOC_LIBRARY_PATH
    # that could be provided by neurodamus-core
    import_modules = []

    def setup_run_environment(self, env):
        env.set("NEURON_INIT_MPI", "0")
        env.unset("PMI_RANK")
