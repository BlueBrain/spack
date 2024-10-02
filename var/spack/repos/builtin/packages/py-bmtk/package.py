# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBmtk(PythonPackage):
    """The Brain Modeling Toolkit"""

    homepage = "https://github.com/AllenInstitute/bmtk"
    pypi = "bmtk/bmtk-1.0.5.tar.gz"

    version("1.1.0", sha256="64fd43e67c5e87cbf737cbd958842cf9dc22784c1a85b08ce490489261cce285")
    version("1.0.8", sha256="9609da6347e74b440a44590f22fc2de0b281fc2eed4c1ee259730c5a8b3c0535")
    version("1.0.7", sha256="11e85098cf3c940a3d64718645f4a24ee13c8a47438ef5d28e054cb27ee01702")
    version("1.0.5", sha256="e0cb47b334467a6d124cfb99bbc67cc88f39f0291f4c39929f50d153130642a4")

    depends_on("py-setuptools", type="build")

    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-sympy", type=("build", "run"))
