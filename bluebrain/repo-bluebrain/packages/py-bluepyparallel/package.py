# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyparallel(PythonPackage):
    """Python library to run embarassingly parallel computations."""

    homepage = "https://github.com/BlueBrain/BluePyParallel"
    git = "https://github.com/BlueBrain/BluePyParallel.git"
    pypi = "bluepyparallel/bluepyparallel-0.2.1.tar.gz"

    version("0.2.1", sha256="ac5c463fd12d8e529369b2da9ac5f017f34fbb77bb7adbe74b913ad781b4d93d")
    version("0.2.0", sha256="1b90ca2bf0cfb0c6f632b9d6366b18b418f3ace2c16ac97a0fe601c2f6609130")
    version("0.0.9", sha256="01496604355241b7baf373418cd829518f70632d3516d162b35ae8990a2872be")

    depends_on("py-setuptools", type="build")

    depends_on("py-pandas@0.24:", type="run", when="@:0.0.5")
    depends_on("py-pandas@1.3:", type="run", when="@0.0.8:")
    depends_on("py-dask+dataframe+distributed@2.30:", type="run", when="@:0.0.5")
    depends_on("py-dask+dataframe+distributed@2021.11:", type="run", when="@0.0.8:")
    depends_on("py-dask-mpi@2.21.0:", type="run", when="@:0.0.5")
    depends_on("py-dask-mpi@2021.11:", type="run", when="@0.0.8:")
    depends_on("py-mpi4py@3.0.3:", type="run")
    depends_on("py-tqdm@4.28.1:", type="run")
    depends_on("py-sqlalchemy@:1.3", type="run", when="@:0.0.5")
    depends_on("py-sqlalchemy@:1.4", type="run", when="@0.0.8:")
    depends_on("py-sqlalchemy-utils@0.36:", type="run", when="@:0.0.5")
    depends_on("py-sqlalchemy-utils@0.37.2:", type="run", when="@0.0.8:")
    depends_on("py-ipyparallel@6.3:6", type="run", when="@0.0.8:0.1")
    depends_on("py-ipyparallel@6.3:", type="run", when="@0.2.0:")
