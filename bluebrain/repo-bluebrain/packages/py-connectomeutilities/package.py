# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-connectomeutilities
#
# You can edit this file again by typing:
#
#     spack edit py-connectomeutilities
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyConnectomeutilities(PythonPackage):
    """Running topological analyses on detailed models of networks"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/BlueBrain/ConnectomeUtilities"

    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
    url = "https://github.com/BlueBrain/ConnectomeUtilities/archive/refs/tags/v0.4.6.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("Apache-2.0")

    version("0.4.6", sha256="7257fde1df849b92b192d23507d673787308a9ca7d0c706d0edbf5da13aaced6")
    version("0.4.5", sha256="b53bca6d463f2146fa405d3635db3ba79a7c6ee00ad47812b8c1b165e4c93be7")
    version("0.4.2", sha256="8da77fa2c78ee0ec5639ec7773d0a173333fa6383057c858944c363f283153ef")
    version("0.4.0", sha256="7dc1799552dce9b83507e66c8a544b3391bacf247b7bc71d3e86905ba34a336a")
    version("0.3.0", sha256="e1d5eea4ad205471a42175efad49bd7e6a3420628b4baaca4182efd7abca09ff")

    depends_on("py-setuptools@1.0:", type="build")

    depends_on("py-numpy@1.20.0:", type=("build", "run"))
    depends_on("py-h5py@3.6.0:", type=("build", "run"))
    depends_on("py-pandas@2.0.0:", type=("build", "run"))
    depends_on("py-tables@3.6:", type=("build", "run"))
    depends_on("py-scipy@1.8.0:", type=("build", "run"))
    depends_on("py-tqdm@4.50.0:", type=("build", "run"))
    depends_on("py-lazy@1.4:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-libsonata@0.1.10:", type=("build", "run"))
    depends_on("py-bluepysnap@1.0.0:", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))

    def config_settings(self, spec, prefix):
        # FIXME: Add configuration settings to be passed to the build backend
        # FIXME: If not needed, delete this function
        settings = {}
        return settings
