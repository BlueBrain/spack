# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArchngv(PythonPackage):
    """Building workflow and circuit API for Neuro-Glia-Vascular circuits."""

    homepage = "https://github.com/BlueBrain/ArchNGV"
    pypi = "archngv/archngv-3.3.0.tar.gz"

    version("3.3.0", sha256="dc7a909793b189b5ff44e4c27de77203e69ecfcc25607de4d4e33f553f738428")

    depends_on("py-setuptools@42:", type="build")

    depends_on("py-numpy@1.22:", type=("build", "run"))
    depends_on("py-h5py@3.1.0:", type=("build", "run"))
    depends_on("py-scipy@1.5.0:", type=("build", "run"))
    depends_on("py-libsonata@0.1.21:", type=("build", "run"))
    depends_on("py-bluepysnap@1.0:", type=("build", "run"))
    depends_on("py-cached-property@1.5:", type=("build", "run"))
    depends_on("py-voxcell@3.0.0:", type=("build", "run"))
    depends_on("py-vascpy@0.1.0:", type=("build", "run"))
    depends_on("py-trimesh@2.38.10:", type=("build", "run"))
    # needed for trimesh marchingcubes
    depends_on("py-scikit-image", type=("build", "run"))

    # "all" optional dependencies
    depends_on("py-ngv-ctools@1.0.0:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-numpy-stl@2.10", type=("build", "run"))
    depends_on("py-openmesh@1.1.2:", type=("build", "run"))
    depends_on("py-pyyaml@5.0:", type=("build", "run"))
    depends_on("py-pandas@1.1.0:", type=("build", "run"))
    depends_on("py-multivoro", type=("build", "run"))
    depends_on("py-morphio@3.2.0:", type=("build", "run"))
    depends_on("py-morph-tool@2.4.0:", type=("build", "run"))
    depends_on("snakemake@5.0:", type=("build", "run"))
    depends_on("py-tmd@2.0.11:", type=("build", "run"))
    depends_on("py-neurots@3.4.0:", type=("build", "run"))
    depends_on("py-diameter-synthesis@0.5.4", type=("build", "run"))

    depends_on("py-dask+distributed@2022.04.1:", type=("build", "run"))
    depends_on("py-distributed@2.0:", type=("build", "run"))
    depends_on("py-dask-mpi@2.0:", type=("build", "run"))

    depends_on("py-brain-indexer@3.0.0:", type=("build", "run"))
    depends_on("py-atlas-commons@0.1.4:", type=("build", "run"))
    depends_on("py-meshio@5.3.4", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/unit")
