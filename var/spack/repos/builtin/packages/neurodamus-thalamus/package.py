# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusThalamus(NeurodamusModel):
    """FIXME: Put a proper description of your package here."""

    homepage = "ssh://bbpcode.epfl.ch/sim/models/thalamus"
    git      = "ssh://bbpcode.epfl.ch/sim/models/thalamus"

    version('master', git=git, branch='master')

    resource(
       name='neocortex',
       git='ssh://bbpcode.epfl.ch/sim/models/neocortex',
       branch='master',
       destination='resources'
    )

    # Override
    _mod_srcs = ('resources/common/mod', 'resources/neocortex/mod', 'mod')

