# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibsonataMpi(PythonPackage):
    """Libsonata Hdf5Reader plugin for collective I/O."""

    homepage = "https://github.com/BlueBrain/libsonata-mpi"
    git = "https://github.com/BlueBrain/libsonata-mpi.git"
    url = "https://github.com/BlueBrain/libsonata-mpi-v0.0.0.tar.gz"

    version("develop", branch="main", get_full_repo=True, submodules=True)

    version("0.0.1.1", commit="a9c97df578f762f286fad3555e4997ccce5d87b1")
    version("0.0.1", tag="0.0.1", submodules=True)

    depends_on("cmake@3.18:", type="build")

    depends_on("py-mpi4py", type=("build", "link", "run"))
    depends_on("py-libsonata@0.1.25:", type="run")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
