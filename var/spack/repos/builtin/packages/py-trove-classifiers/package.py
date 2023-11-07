# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTroveClassifiers(PythonPackage):
    """Canonical source for classifiers on PyPI."""

    homepage = "https://github.com/pypa/trove-classifiers"
    pypi = "trove-classifiers/trove-classifiers-2023.10.18.tar.gz"

    version(
        "2023.10.18", sha256="2cdfcc7f31f7ffdd57666a9957296089ac72daad4d11ab5005060e5cd7e29939"
    )

    depends_on("py-setuptools", type="build")
