##############################################################################
# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hpctm1459(CMakePackage):
    """Disaster Recovery Tool (HPCTM-1459)"""

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BBPHPC/Disaster+Recovery+Tool"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/personal/hpctm-1459.git"

    version("develop", branch="main", submodules=False)
    version("1.4", tag="1.4", submodules=False)
    version("1.3", tag="1.3", submodules=False)
    version("1.2.1", tag="1.2.1", submodules=False)
    version("1.0.2", tag="1.0.2", submodules=False)
    version("1.0.1", tag="1.0.1", submodules=False)
    version("1.0", tag="1.0", submodules=False)

    variant("tests", default=False, description="Enable GitLab CI tests")

    depends_on("cmake", type="build")

    def cmake_args(self):
        args = ["-DHPCTM1459_ENABLE_TESTS=%s" % ("ON" if "+tests" in self.spec else "OFF")]

        if self.spec.satisfies("@1.2.1:"):
            args.extend(["-DCMAKE_CXX_FLAGS=-DHPCTM1459_VERSION=%s" % self.version])

        return args
