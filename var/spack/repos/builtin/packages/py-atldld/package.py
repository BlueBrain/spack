# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyAtldld(PythonPackage):
    """Search, download, and prepare brain atlas data."""

    homepage = "atlas-download-tools.rtfd.io"
    git = "https://github.com/BlueBrain/Atlas-Download-Tools.git"

    maintainers = ["EmilieDel", "jankrepl", "Stannislav"]

    version("0.3.2", tag="v0.3.2")
    version("0.3.1", tag="v0.3.1")
    version("0.3.0", tag="v0.3.0")
    version("0.2.2", tag="v0.2.2")

    # Build dependencies
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-pillow", type="run")
    depends_on("py-appdirs", type="run")
    depends_on("py-click", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-opencv-python", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-requests", type="run")
    depends_on("py-scikit-image", type="run")
