# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-connectome-manipulator
#
# You can edit this file again by typing:
#
#     spack edit py-connectome-manipulator
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyConnectomeManipulator(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://bbpgitlab.epfl.ch/conn/structural/connectome_manipulator"
    git = "git@bbpgitlab.epfl.ch:conn/structural/connectome_manipulator.git"

    version("develop", branch="main")
    version("0.0.1", commit="ce442945")

    depends_on("parquet-converters@0.8.0:", type="run")

    depends_on("bluepysnap@:0:999", type=("build", "run"))
    depends_on("numpy", type=("build", "run"))
    depends_on("progressbar", type=("build", "run"))
    depends_on("scipy", type=("build", "run"))
    depends_on("scikit-learn", type=("build", "run"))
    depends_on("submitit", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))
    depends_on("py-pyarrow", type=("build", "run"))
    depends_on("py-jsonpickle", type=("build", "run"))
    depends_on("py-submitit", type=("build", "run"))
