# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyClick(PythonPackage):
    """"Python composable command line interface toolkit."""

    homepage = "https://click.palletsprojects.com"
    git = "https://github.com/pallets/click.git"

    version("8.0.3", tag="8.0.3")
    version("8.0.2", tag="8.0.2")
    version("8.0.1", tag="8.0.1")
    version("8.0.0", tag="8.0.0")
    version("7.1.2", tag="7.1.2")
    version("7.0", tag="7.0")
    version("6.6", tag="6.6")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
