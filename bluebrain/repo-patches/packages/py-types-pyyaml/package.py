# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPyyaml(PythonPackage):
    """Typing stubs for PyYAML."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-pyyaml/types-PyYAML-5.4.6.tar.gz"

    version("6.0.12.20240917", sha256="d1405a86f9576682234ef83bcb4e6fff7c9305c8b1fbad5e0bcd4f7dbdc9c587")
    version("5.4.6", sha256="745dcb4b1522423026bcc83abb9925fba747f1e8602d902f71a4058f9e7fb662")

    depends_on("py-setuptools", type=("build"))
