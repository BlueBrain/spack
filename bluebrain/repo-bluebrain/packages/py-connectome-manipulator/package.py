# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyConnectomeManipulator(PythonPackage):
    """Connectome generator tool."""

    homepage = "https://github.com/BlueBrain/connectome-manipulator"
    pypi = "connectome-manipulator/connectome_manipulator-1.0.0.tar.gz"

    version("1.0.1", sha256="6908e8a19681da9beda577d4f9e6f0fa518060f2a66b76a1ca0027b30478ac40") # FIXME

    variant(
        "convert",
        default=False,
        description="Enable runtime support of converting output to SONATA",
    )

    depends_on("parquet-converters@0.8.0:", type="run", when="+convert")

    depends_on("py-bluepysnap@3.0.1:", type=("build", "run"))
    depends_on("py-numpy@1.24.3:", type=("build", "run"))
    depends_on("py-pandas@1.5.3:", type=("build", "run"))
    depends_on("py-progressbar@2.5:", type=("build", "run"))
    depends_on("py-scipy@1.10.1:", type=("build", "run"))
    depends_on("py-scikit-learn@1.3.2:", type=("build", "run"))
    depends_on("py-voxcell@3.1.5:", type=("build", "run"))
    depends_on("py-pyarrow+parquet+dataset@10.0.1:", type=("build", "run"))
    depends_on("py-distributed@2023.4.1:", type=("build", "run"))
    depends_on("py-dask-mpi@2022.4.0:", type=("build", "run"))
    depends_on("py-tables@3.8.0:", type=("build", "run"))
