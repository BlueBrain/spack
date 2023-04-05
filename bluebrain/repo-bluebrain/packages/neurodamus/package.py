# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from llnl.util import tty
from spack import *


from .neurodamus_model import NeurodamusModel, copy_all, make_link

class Neurodamus(NeurodamusModel):
    """ The next-generation AllInOne Neurodamus deployment.

    Neurodamus includes BBP's simulation suite with all internal sim models.
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/neurodamus-models"
    git      = "ssh://git@bbpgitlab.epfl.ch/hpc/sim/neurodamus-models.git"

    version('develop', submodules=True)
    # Let the version scheme be different to avoid users loading it by mistake and getting puzzled
    version('2023.04', branch='bump/2023-april', submodules=True)

    depends_on('py-neurodamus', type=('build', 'run'))

    phases = ["build_model", "merge_hoc_mod", "build", "install"]
    models = ("common", "neocortex", "thalamus")
    model_mods_location = {
        "neocortex": "neocortex/mod/v6"
        # other cases it will fetch "<model_name>/mod"
    }

    @run_before("build_model")
    def gather_hoc_mods(self):
        mkdirp("mod", "hoc")
        for model in self.models:
            mod_src = self.model_mods_location.get(model, model + "/mod")
            tty.info(f"Add mods for {model}: {mod_src}")
            copy_all(mod_src, "mod", make_link)
            copy_all(model + "/hoc", "hoc", make_link)
