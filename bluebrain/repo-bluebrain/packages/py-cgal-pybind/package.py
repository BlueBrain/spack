# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCgalPybind(PythonPackage):
    """Python bindings for CGAL"""

    homepage = "https://github.com/BlueBrain/cgal-pybind"
    git = "https://github.com/BlueBrain/cgal-pybind.git"

    version("develop", submodules=True)
    version("0.1.3", tag="cgal-pybind-v0.1.3", submodules=True)
    version("0.1.2", tag="cgal-pybind-v0.1.2", submodules=True)
    version("0.1.1", tag="cgal-pybind-v0.1.1", submodules=True)
    version("0.1.0", tag="cgal_pybind-v0.1.0", submodules=True)

    depends_on("py-setuptools", type="build")
    depends_on('py-setuptools-scm', type='build')
    depends_on("py-wheel", type="build")
    depends_on("cmake", type="build")
    depends_on("ninja", type="build")

    depends_on("boost@1.50:")
    depends_on("cgal")
    depends_on("eigen")
    depends_on("py-pybind11")
    depends_on('py-pytest', type='test')

    depends_on("py-numpy@1.12:", type=("build", "run"))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
