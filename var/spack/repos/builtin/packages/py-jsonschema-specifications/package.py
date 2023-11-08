# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonschemaSpecifications(PythonPackage):
    """The JSON Schema meta-schemas and vocabularies, exposed as a Registry."""

    homepage = "https://github.com/python-jsonschema/jsonschema-specifications"
    pypi = "jsonschema-specifications/jsonschema_specifications-2023.7.1.tar.gz"

    version("2023.7.1", sha256="c91a50404e88a1f6ba40636778e2ee08f6e24c5613fe4c53ac24578a5a7f72bb")

    depends_on("py-hatchling@1.17.1:", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-referencing@0.28:", type=("build", "run"))
    depends_on("py-importlib-resources", when="^python@:3.8", type=("build", "run"))
