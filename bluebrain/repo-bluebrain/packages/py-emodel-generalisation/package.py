# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEmodelGeneralisation(PythonPackage):
    """Python library to generalise electrical models."""

    homepage = "https://github.com/BlueBrain/emodel-generalisation"
    git = "https://github.com/BlueBrain/emodel-generalisation.git"
    pypi = "emodel-generalisation/emodel-generalisation-0.2.5.tar.gz"

    version("0.2.6", sha256="2e5efdcbab78f478931234c7d271dfead56e6ee2b149b09200f962652e1188c5")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-numpy@1.23.5:", type=("build", "run"))
    depends_on("py-scipy@1.10:", type=("build", "run"))
    depends_on("py-pandas@1.5.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-datareuse@0.0.3:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-bluepyopt@1.13.86:", type=("build", "run"))
    depends_on("py-neurom@3.2.2:", type=("build", "run"))
    depends_on("py-efel@3.1:", type=("build", "run"))
    depends_on("py-morph-tool@2.9:", type=("build", "run"))
    depends_on("neuron+python@8.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.6.2:", type=("build", "run"))
    depends_on("py-bluecellulab@1.7.6:", type=("build", "run"))
    depends_on("py-seaborn@0.12.2:", type=("build", "run"))
    depends_on("py-ipyparallel", type=("build", "run"))
    depends_on("py-dask+dataframe+distributed@2023.3.2:", type=("build", "run"))
    depends_on("py-xgboost@1.7.5:1", type=("build", "run"))
    depends_on("py-diameter-synthesis@0.5.4:", type=("build", "run"))
    depends_on("py-voxcell@3.1.6:", type=("build", "run"))
    depends_on("py-sqlalchemy@1.4:", type=("build", "run"))
    depends_on("py-sqlalchemy-utils@0.37.2:", type=("build", "run"))
    depends_on("py-shap@0.41.0:", type=("build", "run"))
    depends_on("py-scikit-learn@1.1.3:", type=("build", "run"))
    depends_on("py-luigi-tools@0.3.4:", type=("build", "run"))

    # MPI dependencies
    depends_on("py-dask-mpi@2022.4:", type=("build", "run"))
    depends_on("py-mpi4py@3.1.1:", type=("build", "run"))
    depends_on("hpe-mpi@2.25.hmpt:", type=("build", "run"))

    def patch(self):
        # The 6 series was last released 4 years ago and messes with dependencies
        filter_file(r'"py-ipyparallel.*"', '"py-ipyparallel"', "setup.py")
