##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel, \
    version_from_model_core_deps


class NeurodamusThalamocortex(NeurodamusModel):
    """Neurodamus with built-in neocortex model
    """
    homepage = "ssh://bbpcode.epfl.ch/sim/models/neocortex"
    git      = "ssh://bbpcode.epfl.ch/sim/models/neocortex"

    resource(
        name="thalamus",
        git="ssh://bbpcode.epfl.ch/sim/models/thalamus",
        tag="1.4"
    )
    resource(
        name="mousify",
        git="ssh://bbpcode.epfl.ch/sim/models/mousify",
        tag="1.4"
    )

    # IMPORTANT: Register versions (only) here to make them stable
    # Final version name is combined e.g. "1.0-3.0.1"
    model_core_dep_v = (
        ('1.4', '3.2.2'),
    )
    version_from_model_core_deps(model_core_dep_v)

    mech_name = "thalamocortex"

    @run_before('build_model')
    def prepare_mods(self):
        copy_all('mousify/mod', 'mod', make_link)
        copy_all('thalamus/mod', 'mod', make_link)
        copy_all('mod/v5', 'mod', make_link)
        copy_all('mod/v6', 'mod', make_link)
        force_remove('mod/optimized')
