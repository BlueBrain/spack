# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluecellulab(PythonPackage):
    """Pythonic Blue Brain simulator access, former BGLibPy"""

    homepage = "https://github.com/BlueBrain/BlueCelluLab"
    pypi = "bluecellulab/bluecellulab-1.7.6.tar.gz"

    version("1.7.6", sha256="a60ec17c44e759b6726c399d764e4220f6641bf3d845fc3fbfe56d07dba9e6d5")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("neuron+python@8", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-matplotlib@3.0.0:", type=("build", "run"))
    depends_on("py-bluepysnap@1.0.7:1", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-typing-extensions@4.8.0", type="run")

    # skip import test, because bluecellulab needs HOC_LIBRARY_PATH
    # that could be provided by neurodamus-core
    import_modules = []

    def setup_run_environment(self, env):
        env.set("NEURON_INIT_MPI", "0")
        env.unset("PMI_RANK")
