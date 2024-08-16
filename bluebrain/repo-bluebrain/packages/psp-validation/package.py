# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PspValidation(PythonPackage):
    """PSP analysis tools"""

    homepage = "https://github.com/BlueBrain/psp-validation"
    git = "https://github.com/BlueBrain/psp-validation.git"
    pypi = "psp-validation/psp_validation-0.6.0.tar.gz"

    version("develop", branch="main")
    version("0.6.0", sha256="5eb879aaa82be53c6f372d77cd7755ea76aeba835f5d1140f675ba4c2a798f84")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-attrs@20.3.0:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-efel@3.0.39:", type=("build", "run"))
    depends_on("py-h5py@3", type=("build", "run"))
    depends_on("py-joblib@0.16:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy@1.10:", type=("build", "run"))
    depends_on("py-pandas@1.3:1", type=("build", "run"))
    depends_on("py-tqdm@4.0:", type=("build", "run"))
    depends_on("py-bluecellulab@2.6.15:", type=("build", "run"))
    depends_on("py-bluepysnap@3", type=("build", "run"))
    depends_on("py-seaborn@0.11:0", type=("build", "run"))
    depends_on("neuron+python@7.8:", type=("build", "run"))
