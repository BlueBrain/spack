# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRpdsPy(PythonPackage):
    """Python bindings to Rust's persistent data structures (rpds)."""

    homepage = "https://github.com/crate-py/rpds"
    pypi = "rpds-py/rpds_py-0.12.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

    version(
        "0.12.0",
        sha256="3c8c0226c71bd0ce9892eaf6afa77ae8f43a3d9313124a03df0b389c01f832de",
        expand=False,
    )

    depends_on("py-setuptools", type="build")
