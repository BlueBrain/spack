# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultivoro(PythonPackage):
    """Python bindings for Voro++ library with OpenMP support."""

    homepage = "https://github.com/eleftherioszisis/multivoro"
    git = "https://github.com/eleftherioszisis/multivoro.git"

    version("develop", branch="main")
    version("0.0.1", tag="v0.0.1")

    depends_on("py-scikit-build-core@0.4.3:", type=("build", "link"))
    depends_on("py-nanobind", type=("build", "link"))

    depends_on("py-numpy", type=("build", "run"))
