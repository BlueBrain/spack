# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyReferencing(PythonPackage):
    """An implementation-agnostic implementation of JSON reference resolution."""

    homepage = "https://github.com/python-jsonschema/referencing"
    pypi = "referencing/referencing-0.30.2.tar.gz"

    version("0.30.2", sha256="794ad8003c65938edcdbc027f1933215e0d0ccc0291e3ce20a4d87432b59efc0")

    depends_on("py-setuptools", type="build")
    depends_on("py-hatchling@1.17.1:", type="build")
    depends_on("py-hatch-vcs", type="build")
