# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *

from .neurodamus_model import NeurodamusModel


class Neurodamus(NeurodamusModel):
    """ The next-generation AllInOne Neurodamus deployment.

    Neurodamus includes BBP's simulation suite with all internal sim models.
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/neurodamus-models"
    git      = "git@bbpgitlab.epfl.ch:hpc/sim/neurodamus-models.git"

    version('develop', submodules=True)
    # For now let the version give a good hint about what we are, to avoid
    # users loading it by mistake and getting puzzled
    version('0.0.1_allInOne', tag='0.0.1', submodules=True)

    depends_on('py-neurodamus', type=('build', 'run'))

    models = ("common", "neocortex", "hippocampus", "thalamus", "mousify")
    phases = ["build_" + model for model in models] + ["install"]

    def model_install_prefix(self, model_name):
        return prefix.lib.join(model_name)

    def _build_model(self, model_name, spec, prefix):
        with working_dir(model_name):
            self.mech_name = model_name
            NeurodamusModel.merge_hoc_mod(
                self, spec, prefix, create_link_if_not_found,
                merge_hoc=False
            )
            ld_args = "-Wl,-rpath," + self.model_install_prefix(model_name).lib
            NeurodamusModel.build(self, spec, prefix, ld_args)

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
                if model_name == "common":
                    self._install_neurodamus_builder_script()
            force_symlink(model_install_prefix.bin.special,
                          prefix.bin.join("special-" + model_name))

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        env.set('MODELS_LIBRARY_PATH', self.prefix.lib)
        env.prepend_path("PYTHONPATH", self.prefix.lib.common.python)


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
