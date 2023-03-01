# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from .sim_model import SimModel, copy_all, make_link


class ModelNeocortex(SimModel):
    """
    The Neocortex neuron mechanisms for (core)Neuron
    """

    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/models/neocortex"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/sim/models/neocortex.git"
    submodules = True

    version("develop", branch="main")
    version("1.10", tag="1.10")
    version("1.9", tag="1.9")
    version("1.1", tag="1.1")
    version("0.3", tag="0.3-1")
    version("0.2", tag="0.2")
    version("0.1", tag="0.1")

    variant("v5", default=True, description="Enable support for previous v5 circuits")
    variant(
        "plasticity",
        default=False,
        description="Use optimized ProbAMPANMDA_EMS and ProbGABAAB_EMS",
    )

    mech_name = "neocortex"

    @run_before("build")
    def prepare_mods(self):
        if self.spec.satisfies("+v5"):
            copy_all("mod/v5", "mod", make_link)
        copy_all("mod/v6", "mod", make_link)
        # Plasticity
        if self.spec.satisfies("+plasticity"):
            copy_all("mod/v6/optimized", "mod", make_link)
