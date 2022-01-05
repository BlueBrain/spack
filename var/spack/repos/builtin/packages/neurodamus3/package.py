# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel
from llnl.util import tty


class Neurodamus3(NeurodamusModel):
    """The Blue Brain Project simulation suite with BBP models"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/neurodamus-models"
    git      = "git@bbpgitlab.epfl.ch:hpc/sim/neurodamus-models.git"

    version('develop', submodules=True)

    models = ("common", "neocortex", "hippocampus", "thalamus", "mousify")
    phases = ["build_" + model for model in models] + ["install"]

    def model_install_prefix(self, model_name):
        return prefix.lib.join(model_name)

    def _build_model(self, model_name, spec, prefix):
        with working_dir(model_name):
            self.mech_name = model_name
            NeurodamusModel.merge_hoc_mod(self, spec, prefix, create_link_if_not_found)
            extra_link_args = "-Wl,-rpath," + self.model_install_prefix(model_name).lib
            NeurodamusModel.build(self, spec, prefix, extra_link_args)

    def build_common(self, spec, prefix):
        self._build_model("common", spec, prefix)

    def build_neocortex(self, spec, prefix):
        copy_all('neocortex/mod/v6', 'neocortex/mod')
        self._build_model("neocortex", spec, prefix)

    def build_hippocampus(self, spec, prefix):
        self._build_model("hippocampus", spec, prefix)

    def build_thalamus(self, spec, prefix):
        self._build_model("thalamus", spec, prefix)

    def build_mousify(self, spec, prefix):
        self._build_model("mousify", spec, prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for model_name in self.models:
            model_install_prefix = self.model_install_prefix(model_name)
            with working_dir(model_name):
                self._install_src(prefix, model_name)
                self._install_binaries(model_install_prefix)
            force_symlink(model_install_prefix.bin.special,
                          prefix.bin.join("special-" + model_name))


def create_link_if_not_found(src, dst):
    """
    Args:
        src (str): The path of the file to create a link to
        dst (str): The link destination path (may be a directory)
    """
    if os.path.isdir(dst):
        dst_dir = dst
        dst = join_path(dst, os.path.basename(src))
    else:
        dst_dir = os.path.dirname(dst)
    if os.path.exists(dst):
        return
    if not os.path.isabs(src):
        src = os.path.relpath(src, dst_dir)  # update path relation
    os.symlink(src, dst)
