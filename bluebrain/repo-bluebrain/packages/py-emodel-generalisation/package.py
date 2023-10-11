# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEmodelGeneralisation(PythonPackage):
    """Python library to generalise electrical models."""

    homepage = "https://github.com/BlueBrain/emodel-generalisation"
    git = "ssh://git@github.com:BlueBrain/emodel-generalisation.git"

    version("0.0.1", tag="emodel-generalisation-0.0.1")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-bluepyopt@1.13.86:", type=("build", "run"))
    depends_on("py-neurom@3.0:3", type=("build", "run"))
    depends_on("py-efel@3.1:", type=("build", "run"))
    depends_on("py-configparser", type=("build", "run"))
    depends_on("py-morph-tool@2.8:", type=("build", "run"))
    depends_on("py-fasteners@0.16:", type=("build", "run"))
    depends_on("neuron+python@8.0:", type=("build", "run"))
    depends_on("py-jinja2@3.0.3", when="@0.0.11:", type=("build", "run"))
    depends_on("py-click@7.0:", when="@0.0.8", type=("build", "run"))
    depends_on("py-matplotlib@2.2:", type=("build", "run"))
    depends_on("py-bluepyparallel@0.0.5:", when="@0.0.8", type=("build", "run"))
    depends_on("py-bluecellulab@1.5.2:", type=("build", "run"))
    depends_on("py-seaborn@0.11:", when="@0.0.8", type=("build", "run"))
