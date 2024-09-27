# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFzTdRecipe(PythonPackage):
    """Python package to read and modify the definitions and parameters used in circuit
    building."""

    homepage = "https://github.com/BlueBrain/fz-td-recipe"
    git = "https://github.com/BlueBrain/fz-td-recipe.git"
    pypi = "fz-td-recipe/fz_td_recipe-0.2.2.tar.gz"

    version("develop", branch="main")
    version("0.2.4", sha256="e902ca32b7c94306adbd0763dbf38b39fec4e4fdb41bc3531d4c3030a23a3004")
    version("0.2.2", sha256="34eded0440c065c5a3fabe43ed0c736a6b4174b8f6ac24a4275818954d6cabda")
    version("0.1.2", tag="fz-td-recipe-v0.1.2")

    depends_on("py-setuptools", type="build", when="@0.1.2")
    depends_on("py-hatchling", type="build", when="@0.2.2:")
    depends_on("py-hatch-vcs", type="build", when="@0.2.2:")

    depends_on("py-click", type=("build", "run"), when="@0.2:")
    depends_on("py-jsonschema", type=("build", "run"), when="@0.2:")
    depends_on("py-lxml@:4", type=("build", "run"), when="@:0.2.2")
    depends_on("py-lxml@:4", type=("build", "run"), when="@0.2.4:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"), when="@0.2.2:")
