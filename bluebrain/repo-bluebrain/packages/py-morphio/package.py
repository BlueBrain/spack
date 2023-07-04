# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMorphio(PythonPackage):
    """Python library for reading / writing morphology files"""

    homepage = "https://github.com/BlueBrain/MorphIO"
    git = "https://github.com/BlueBrain/MorphIO.git"
    pypi = "morphio/MorphIO-3.3.2.tar.gz"

    version("develop", branch="master", submodules=True)
    version("unifurcation", branch="unifurcation", submodules=True)

    version("3.3.6", sha256="0f2e55470d92a3d89f2141ae905ee104fd16257b93dafb90682d90171de2f4e6")
    version("3.3.5", sha256="9e6cfebaea32080131b2b08a4a32dfbe92b18427a3e557861e27c4131f7542ac")
    version("3.3.4", sha256="b70c6884e9b835560501f798c75c9cc7eaf3162cba1d930b5a9b854bb9ea60dc")
    version("3.3.3", sha256="f6d91970cfd734b2e5fb8f9239a0bfa00519fe082dd8e403e4cc204dbdf0a9fa")
    version("3.3.2", sha256="fc961defbfbfb3f11360954fb3ec51373eaff25b154fa31d6b31decca6937780")
    version("3.1.1", sha256="ad9f0e363f09f03c6eda54f5f3b006d204236677d2f2c9675421e0441033a503")
    version("2.7.1", sha256="3f3e2229da85e874527775fce080f712b6dc287edc44b90b6de35d17b34badff")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("ninja", type="build")
    depends_on("cmake@3.2:", type="build")
    depends_on("py-numpy@1.14.1:", type="run")
    depends_on("hdf5")
