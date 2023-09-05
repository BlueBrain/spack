# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepy(PythonPackage):
    """Pythonic Blue Brain data access API"""

    homepage = "https://bbpgitlab.epfl.ch/nse/bluepy"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/bluepy.git"

    version("develop", branch="main")
    version("2.5.2", tag="bluepy-v2.5.2")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-libsonata@0.1.7:0", type=("build", "run"))
    depends_on("py-pandas@1,2.0.1:2", type=("build", "run"))
    depends_on("py-bluepy-configfile@0.1.20:", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-h5py@3.0.1:3", type=("build", "run"))
    depends_on("py-morph-tool@2.4.3:2", type=("build", "run"))
    depends_on("py-morphio@3.0.1:3", type=("build", "run"))
    depends_on("py-voxcell@3", type=("build", "run"))
    depends_on("py-cached-property@1.0:", type=("build", "run"))
    depends_on("brion+python@3.3.0:3", type=("build", "run"))

    @property
    def import_modules(self):
        # bluepy.index requires libFLATIndex, unavailable on spack
        modules = super(PyBluepy, self).import_modules
        return [m for m in modules if m != "bluepy.index"]
