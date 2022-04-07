# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyArchngv(Package):
    """Building workflow and circuit API for Neuro-Glia-Vascular circuit."""

    homepage = "https://bbpgitlab.epfl.ch/nse/ArchNGV"
    url      = "git@bbpgitlab.epfl.ch:nse/ArchNGV.git"

    version("develop", branch="main")
    version("2.0.0", tag="ArchNGV-v2.0.0")

    depends_on("py-setuptools@42:", type="build")

    depends_on("py-numpy@1.19.5:", type="run")
    depends_on("py-scipy@1.5.0:", type="run")
    depends_on("py-h5py@3.1.0:", type="run")
    depends_on("py-libsonata@0.1.8:0.99", type="run")
    depends_on("py-bluepysnap@0.13:0.99", type="run")
    depends_on("py-cached-property@1.5:", type="run")
    depends_on("py-voxcell@3.0.0:", type="run")
    depends_on("py-vascpy@0.1.0:", type="run")

    depends_on("py-ngv-ctools@1.0:", type="run")
    depends_on("spatial-index@0.4.2:0.99", type="run")
    depends_on("py-bluepy-configfile@0.1.11:", type="run")
    depends_on("py-click@7.0:7.99", type="run")
    depends_on("py-numpy-stl@2.10:2.99", type="run")
    depends_on("py-openmesh@1.1.2:1.99", type="run")
    depends_on("py-pyyaml@5.0:5.99", type="run")
    depends_on("py-pandas@1.1.0:1.99", type="run")
    depends_on("py-tess@0.3.2", type="run")
    depends_on("py-morphio@3.3.1:", type="run")
    depends_on("py-morph-tool@2.4.0:", type="run")
    depends_on("snakemake@5.0:5.99", type="run")
    depends_on("py-tmd@2.0.11:", type="run")
    depends_on("py-tns@2.5.0", type="run")
    depends_on("py-diameter-synthesis@0.2.5", type="run")
    depends_on("py-trimesh@2.38.10:", type="run")

    depends_on("py-dask+distributed+bag@2.0:2.99", type="run")
    depends_on("py-distributed@2.0:2.99", type="run")
    depends_on("py-dask-mpi@2.0:2.99", type="run")
