# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusHippocampus(NeurodamusModel):
    """FIXME: Put a proper description of your package here."""

    homepage = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"
    git      = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"

    version('master', git=git, branch='master')

