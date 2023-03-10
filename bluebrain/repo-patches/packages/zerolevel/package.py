# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zerolevel(CMakePackage):
    """
    Intel API to provide direct-to-metal interfaces to offload accelerator
    devices.
    """

    homepage = "https://spec.oneapi.io/level-zero/latest/index.html"
    git = "https://github.com/oneapi-src/level-zero.git"
    generator = "Ninja"

    version("1.9.9", tag="v1.9.9")

    depends_on("cmake@3.1:", type="build")
    depends_on("ninja", type="build")
