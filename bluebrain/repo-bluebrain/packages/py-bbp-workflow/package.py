# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBbpWorkflow(PythonPackage):
    """Blue Brain Workflow."""

    homepage = "https://bbpgitlab.epfl.ch/nse/bbp-workflow"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/bbp-workflow.git"

    version("3.1.38", tag="bbp-workflow-v3.1.38")

    depends_on("py-setuptools", type=("build"))

    depends_on("py-requests-unixsocket", type="run")
    depends_on("py-dask+diagnostics", type="run")
    depends_on("py-distributed", type="run")
    depends_on("py-luigi", type="run")
    depends_on("py-jsonschema", type="run")
    depends_on("py-luigi-tools", type="run")
    depends_on("py-sh@:1", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-bluepy", type="run")
    depends_on("py-bluepy-configfile", type="run")
    depends_on("py-bluepysnap", type="run")
    depends_on("py-voxcell", type="run")
    depends_on("py-entity-management", type="run")
    depends_on("py-xarray", type="run")
    depends_on("py-pint-xarray", type="run")
    depends_on("py-cheetah3", type="run")
    depends_on("py-elephant", type="run")
    depends_on("py-neo", type="run")
    depends_on("py-pyarrow+parquet", type="run")
    depends_on("py-click", type="run")
    depends_on("py-cwl-luigi", type="run")
    depends_on("py-cwl-registry", type="run")
    depends_on("py-brayns", type="run")
    depends_on("py-bluepyemodel", type="run")
    depends_on("py-bluepyemodelnexus", type="run")

    # extra deps to include in the module
    # depend on a version with BBP ca root patch
    depends_on("py-certifi@2021.10.8", type="run")
    # enable serialization of xarray to zarr compressed array
    depends_on("py-zarr", type="run")
    # enable workflow tasks launch jupyter notebooks
    depends_on("py-notebook", type="run")
    # enable workflow tasks create ipyparallel cluster
    depends_on("py-ipyparallel", type="run")
    # rdflib plugins pull this from python-daemon
    depends_on("py-docutils", type="run")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec["py-distributed"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-notebook"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-ipython"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-ipyparallel"].prefix.bin)
        env.prepend_path("PATH", self.spec["py-luigi"].prefix.bin)
