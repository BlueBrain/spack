# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMorphoKit(PythonPackage):
    """Python library for reading / writing morphology files"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/morpho-kit"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/morpho-kit.git"

    submodules = True

    version("develop", branch="main")
    version("0.3.5", commit="aee8232e8acb7add30e210b11fe2528fa658fb9f")
    version("0.3.4", tag="v0.3.4")
    version("0.3.3", tag="0.3.3")
    version("0.3.2", tag="v0.3.2")
    version("0.2.0", tag="v0.2.0")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("morphio@2.3.9:", type=("build", "link"), when="@0.3.4")
    depends_on("morphio@3.3.5:", type=("build", "link"), when="@0.3.5:")

    depends_on("cmake@3.2:", type="build")
    depends_on("py-numpy", type="run")
    depends_on("boost", when="@0.2.0")

    patch("h5.patch", when="@0.3.2")
