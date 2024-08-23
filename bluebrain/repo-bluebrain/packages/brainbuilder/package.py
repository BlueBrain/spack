# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brainbuilder(PythonPackage):
    """Miscellaneous circuit building utilities"""

    homepage = "https://github.com/BlueBrain/brainbuilder"
    git = "https://github.com/BlueBrain/brainbuilder.git"
    pypi = "brainbuilder/brainbuilder-0.20.1.tar.gz"

    version("0.20.1", sha256="d46c3dc831dbac24a926a6e7b31a9eeea06bcc5fa500b84efb8153e27b56fac3")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@8.0.0:", type="build")

    depends_on("py-joblib@1.0.1:", type=("build", "run"))
    depends_on("py-click@7:8", type=("build", "run"))
    depends_on("py-h5py@3.1.0:", type=("build", "run"))
    depends_on("py-jsonschema@3.2.0:", type=("build", "run"))
    depends_on("py-lxml@3.3:", type=("build", "run"))
    depends_on("py-numpy@1.9:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.3.1:", type=("build", "run"))
    depends_on("py-scipy@0.13:", type=("build", "run"))
    depends_on("py-tqdm@4.0:", type=("build", "run"))
    depends_on("py-bluepy@2.1:", type=("build", "run"))
    depends_on("py-libsonata@0.1.8:", type=("build", "run"))
    depends_on("py-voxcell@3.1.1:", type=("build", "run"))
    depends_on("py-morphio@3", type=("build", "run"))
    depends_on("py-bluepysnap@1.0.3:", type=("build", "run"))
