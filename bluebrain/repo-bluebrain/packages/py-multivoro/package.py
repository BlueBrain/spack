# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultivoro(PythonPackage):
    """Python bindings for Voro++ library with OpenMP support."""

    homepage = "https://github.com/eleftherioszisis/multivoro"
    git = "https://github.com/eleftherioszisis/multivoro.git"
    pypi = "multivoro/multivoro-0.1.0.tar.gz"

    version("0.1.1", sha256="dd15ff7c54f83e099623d2874b58309fbda4f59cec02b351252d6fb7a7551e31")

    depends_on("py-scikit-build-core@0.4.3:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-nanobind", type="build")

    depends_on("py-numpy", type=("build", "run"))

    def patch(self):
        filter_file(
            """USE_OpenMP = {env="USE_OpenMP", default="OFF"}""",
            "USE_OpenMP = \"OFF\"",
            "pyproject.toml",
        )

    def setup_build_environment(self, env):
        for pth in self.spec["py-nanobind"].package.cmake_prefix_paths:
            env.append_path("CMAKE_PREFIX_PATH", pth)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test(self):
        python("-m", "pytest", "tests")
