# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyAtldld(PythonPackage):
    """Search, download, and prepare brain atlas data."""

    homepage = "atlas-download-tools.rtfd.io"
    pypi = "atldld/atldld-0.3.3.tar.gz"

    maintainers = ["EmilieDel", "jankrepl", "Stannislav"]

    version('0.3.3', sha256='c50dfabed5f318f15fdddc031d48e0cfd2b15846d307fbc57c797fa35edfef40')
    version('0.3.2', sha256='e39392ebd2ffb675b5b98016f5982da6cbcca0249622e0e6509c98c6f07ee3bc')
    version('0.3.1', sha256='5b4b724392378771baa14cf15058f1f8ab33c587ff7a9f99e3278135dfb7ff64')
    version('0.3.0', sha256='78186f994262505ebae62ad78858f0ff4ec95a1c7e5aa9935871c2485aa4d947')
    version('0.2.2', sha256='4bdbb9ccc8e164c970940fc729a10bf883a67035e8c636261913cecb351835d3')

    # Build dependencies
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-appdirs", when="@0.3.1:", type=("build", "run"))
    depends_on("py-click@8:", when="@0.3.0:", type=("build", "run"))
    depends_on("py-dataclasses", when="@0.3.1: ^python@3.6", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-opencv-python", type=("build", "run"))
    depends_on("py-pandas", when="@:0.3.2", type=("build", "run"))
    depends_on("py-pillow", when="@0.3.1:", type=("build", "run"))
    depends_on("py-requests", when="@:0.3.2", type=("build", "run"))
    depends_on("py-responses", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
