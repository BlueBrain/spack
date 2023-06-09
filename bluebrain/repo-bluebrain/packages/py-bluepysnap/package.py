# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepysnap(PythonPackage):
    """Blue Brain SNAP is a Python library for accessing BlueBrain circuit models
    represented in SONATA format."""

    homepage = "https://github.com/BlueBrain/snap"
    git = "https://github.com/BlueBrain/snap.git"
    pypi = "bluepysnap/bluepysnap-0.12.0.tar.gz"

    version("develop", branch="master")
    version("1.0.5", sha256="8c9c50bcd7282a96c006c5c7ddffe53542378abc1d400bdf82e91b770d7224e0")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-cached-property@1.0:", type=("build", "run"))
    depends_on("py-h5py@3.0.1:3", type=("build", "run"))
    depends_on("py-jsonschema@4", type=("build", "run"), when="@1:")
    depends_on("py-libsonata@0.1.21:", type=("build", "run"))
    depends_on("py-morphio@3", type=("build", "run"))
    depends_on("py-morph-tool@2.4.3:2", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:1", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-more-itertools@8.2.0:", type=("build", "run"))
    depends_on("spatial-index@1.2.1:", type=("build", "run"))
