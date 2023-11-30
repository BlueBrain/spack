# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyDatareuse(PythonPackage):
    """Util package to reuse computed datasets"""

    git = "https://github.com/arnaudon/datareuse"
    pypi = "datareuse/datareuse-0.0.3.tar.gz"

    version("0.0.3", sha256="63b03ae4acda22e93911adde0325818842bf65e42291ecfc88706e735a190749")

    depends_on("py-pandas@1.0.2:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
