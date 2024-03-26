# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class NeurodamusModels(CMakePackage):
    """Neuroscientific models to be used with Neurodamus"""

    homepage = "https://github.com/BlueBrain/neurodamus-models"
    git = "ssh://git@github.com/BlueBrain/neurodamus-models.git"

    version("develop", branch="cfaire")
    version("6.6.6", commit="d66d0de8741543497bb127998deba7a5e3f7de42")
    version("6.6.7", commit="8e21f8e16e037d0f1042d4585b1417f083bd1cea")
    version("6.6.8", commit="506f1cb7dbf59d9dfca835245597e59e144ed24a")
    version("6.6.9", commit="2cc59da34d22633df5baff3a2ec282e93de54b97")
    version("6.7.0", commit="0eee2cc6a4d8f84f3f7980fc6d9c88f5a5f258df")
    version("6.7.1", commit="3ae2eb94fc8f415d32b89b4003d12b24f4d03384")
    version("6.7.2", commit="4d89b24a46a36e2b9f1f2d2ee108d7f1c478e64f")
    version("6.7.3", commit="2dc61b533c1b036c3b52ed0aa14393932d269842")
    version("6.7.4", commit="b848572f214f799ccb0ccb8615ceb8b925f6dca9")

    variant("caliper", default=False, description="Enable Caliper instrumentation")
    variant("coreneuron", default=False, description="Enable CoreNEURON support")

    variant(
        "model",
        default="neocortex",
        values=("hippocampus", "neocortex", "thalamus"),
        multi=False,
        description="Which brain region mechanism to enable",
    )
    variant("ngv", default=False, when="model=neocortex", description="Enable NGV mechanisms")
    variant(
        "metabolism", default=False, when="model=neocortex", description="Enable metabolism mechanisms"
    )
    variant(
        "plasticity", default=False, when="model=neocortex", description="Enable plasticity related mechanisms"
    )
    variant("v5", default=True, when="model=neocortex", description="Enable V5 circuit mechanisms")

    depends_on("neuron", type=("build", "link", "run"))
    depends_on("neuron+coreneuron", when="+coreneuron", type=("build", "link", "run"))
    depends_on("neuron+caliper", when="+caliper", type=("build", "link", "run"))

    depends_on("py-neurodamus", type=("build", "run"))
    depends_on("libsonata-report")

    def cmake_args(self):
        args = [
            self.define("NEURODAMUS_CORE_DIR", self.spec["py-neurodamus"].package.datadir),
            self.define_from_variant("NEURODAMUS_MECHANISMS", "model"),
            self.define_from_variant("NEURODAMUS_ENABLE_CORENEURON", "coreneuron"),
            self.define_from_variant("NEURODAMUS_NCX_METABOLISM", "metabolism"),
            self.define_from_variant("NEURODAMUS_NCX_NGV", "ngv"),
            self.define_from_variant("NEURODAMUS_NCX_PLASTICITY", "plasticity"),
            self.define_from_variant("NEURODAMUS_NCX_V5", "v5"),
        ]
        return args

    def setup_build_environment(self, env):
        env.unset("LC_ALL")

    def setup_run_environment(self, env):
        mech = self.spec.variants["model"].value
        env.set(f"NEURODAMUS_{mech.upper()}_ROOT", self.prefix)
        env.set("HOC_LIBRARY_PATH", self.prefix.share.join(f"neurodamus_{mech}").hoc)
        if "+coreneuron" in self.spec:
            env.set("CORENEURONLIB", self.prefix.lib + "/libcorenrnmech.so")
        for libnrnmech_name in find(self.prefix.lib, "libnrnmech*.so", recursive=False):
            env.prepend_path("NRNMECH_LIB_PATH", libnrnmech_name)
            env.prepend_path("BLUECELLULAB_MOD_LIBRARY_PATH", libnrnmech_name)

        # ENV variables to enable Caliper with certain settings
        if "+caliper" in self.spec:
            env.set("NEURODAMUS_CALI_ENABLED", "true")  # Needed for slurm.taskprolog
            env.set("CALI_MPIREPORT_FILENAME", "/dev/null")  # Prevents 'stdout' output
            env.set("CALI_CHANNEL_FLUSH_ON_EXIT", "false")
            env.set(
                "CALI_MPIREPORT_LOCAL_CONFIG",
                "SELECT sum(sum#time.duration), \
                                                        inclusive_sum(sum#time.duration) \
                                                    GROUP BY prop:nested",
            )
            env.set(
                "CALI_MPIREPORT_CONFIG",
                "SELECT annotation, \
                        mpi.function, \
                        min(sum#sum#time.duration) as exclusive_time_rank_min, \
                        max(sum#sum#time.duration) as exclusive_time_rank_max, \
                        avg(sum#sum#time.duration) as exclusive_time_rank_avg, \
                        min(inclusive#sum#time.duration) AS inclusive_time_rank_min, \
                        max(inclusive#sum#time.duration) AS inclusive_time_rank_max, \
                        avg(inclusive#sum#time.duration) AS inclusive_time_rank_avg, \
                        percent_total(sum#sum#time.duration) AS exclusive_time_pct, \
                        inclusive_percent_total(sum#sum#time.duration) AS inclusive_time_pct \
                    GROUP BY prop:nested FORMAT json",
            )
            env.set("CALI_SERVICES_ENABLE", "aggregate,event,mpi,mpireport,timestamp")
            env.set("CALI_MPI_BLACKLIST", "MPI_Comm_rank,MPI_Comm_size,MPI_Wtick,MPI_Wtime")
