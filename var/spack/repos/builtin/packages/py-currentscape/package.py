# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCurrentscape(PythonPackage):
    """Module to easily plot currentscape."""

    homepage = "https://bbpgitlab.epfl.ch/cells/currentscape"
    git = "ssh://git@bbpgitlab.epfl.ch/cells/currentscape.git"

    version("develop", branch="master")
    version("0.0.10", tag="currentscape-v0.0.10")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-palettable", type=("build", "run"))
