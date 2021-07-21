# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class SpatialIndex(PythonPackage):
    """Spatial indexer for geometries and morphologies"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/SpatialIndex"
    git      = "git@bbpgitlab.epfl.ch:hpc/SpatialIndex.git"
    url      = "git@bbpgitlab.epfl.ch:hpc/SpatialIndex.git"

    version('develop', branch='master', submodules=True)
    version('0.2.1', tag='0.2.1', submodules=True)
    version('0.1.0', tag='0.1.0', submodules=True)

    depends_on("py-setuptools")
    depends_on("cmake")
    depends_on("boost@:1.70.0")
    depends_on("py-numpy",       type=("build", "run"))
    depends_on("py-morphio",     type="run")
    depends_on("py-mvdtool~mpi", type="run")
    depends_on("py-morpho-kit",  type="run")
    depends_on("py-numpy-quaternion", type="run", when="@0.2.1:")
    depends_on("py-libsonata",   type="run", when="@0.2.2:")

    @run_after('install')
    def install_headers(self):
        install_tree('include', self.prefix.include)
