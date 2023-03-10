# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyAtldld(PythonPackage):
    """Search, download, and prepare brain atlas data."""

    homepage = "atlas-download-tools.rtfd.io"
    git = "https://github.com/BlueBrain/Atlas-Download-Tools.git"
    pypi = "atldld/atldld-0.3.4.tar.gz"

    maintainers = ["EmilieDel", "jankrepl", "Stannislav"]

    version("0.3.4", sha256="4385d279e984864814cdb586d19663c525fe2c1eef8dd4be19e8a87b8520a913")

    # Build dependencies
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-appdirs", when="@0.3.1:", type=("build", "run"))
    depends_on("py-click@8:", when="@0.3.0:", type=("build", "run"))
    depends_on("py-dataclasses", when="@0.3.1: ^python@3.6", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("opencv+python3+python_bindings_generator+imgproc", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pillow", when="@0.3.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-responses", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))

    def setup_run_environment(self, env):
        spec = self.spec
        env.prepend_path(
            "LD_LIBRARY_PATH",
            os.path.join(
                spec["intel-oneapi-mkl"].prefix,
                "compiler",
                str(spec["intel-oneapi-mkl"].version),
                "linux",
                "compiler",
                "lib",
                "intel64_lin",
            ),
        )
