# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstrovascpy(PythonPackage):
    """
    Vasculature blood flow computation and impact of astrocytic
    endfeet on vessels
    """

    homepage = "https://github.com/BlueBrain/AstroVascPy"

    url = "https://github.com/BlueBrain/AstroVascPy/releases/tag/0.1"

    maintainers("tristan0x")

    version("0.1", sha256="1e9b2036e9c1ce4cb0650612c0be2e7e7b142754e1550dfbfb0b757cee4f8bdd")

    variant("vtk", default=False, description="add VTK support (mainly for visualization)")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-click", type="build")
    depends_on("py-cached-property", type="build")
    depends_on("py-coverage", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-h5py", type="build")
    depends_on("py-libsonata", type="build")
    depends_on("py-matplotlib", type="build")
    depends_on("py-morphio", type="build")
    depends_on("py-networkx", type="build")
    depends_on("py-numpy", type="build")
    depends_on("py-pandas", type="build")
    depends_on("petsc", type="build")
    depends_on("py-petsc4py", type="build")
    depends_on("py-psutil", type="build")
    depends_on("py-pyyaml", type="build")
    depends_on("py-scipy", type="build")
    depends_on("py-seaborn", type="build")
    depends_on("py-tables", type="build")
    depends_on("py-tqdm", type="build")
    depends_on("py-trimesh", type="build")
    depends_on("py-vascpy", type="build")
    depends_on("vtk+python", type="build", when="+vtk")
    depends_on("py-wheel ", type="build")

    depends_on("py-pytest", type="test")
    depends_on("py-pytest-mpi", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
