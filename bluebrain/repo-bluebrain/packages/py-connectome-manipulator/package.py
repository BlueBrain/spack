# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyConnectomeManipulator(PythonPackage):
    """Connectome generator tool."""

    homepage = "https://github.com/BlueBrain/connectome-manipulator"
    pypi = "connectome-manipulator/connectome_manipulator-1.0.0.tar.gz"

    version("1.0.0", sha256="f77151bc7569f9d18d77dad04cd9fa24c403989ea28a1811566cc49332a785ef")

    # Fixes dependency and Python version requirements
    patch("dependencies.patch", when="@1.0.0")

    variant(
        "convert",
        default=False,
        description="Enable runtime support of converting output to SONATA",
    )

    depends_on("parquet-converters@0.8.0:", type="run", when="+convert")

    depends_on("py-bluepysnap@3.0.1:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-progressbar", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))
    depends_on("py-pyarrow+parquet+dataset", type=("build", "run"))
    depends_on("py-distributed", type=("build", "run"))
    depends_on("py-dask-mpi", type=("build", "run"))
    depends_on("py-tables", type=("build", "run"))
