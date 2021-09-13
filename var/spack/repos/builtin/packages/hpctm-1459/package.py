##############################################################################
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Hpctm1459(CMakePackage):
    """HPCTM1459"""

    homepage = "https://bbpteam.epfl.ch/project/issues/browse/HPCTM-1459"
    url      = "git@bbpgitlab.epfl.ch:hpc/user/hpctm-1459.git"
    git      = "git@bbpgitlab.epfl.ch:hpc/user/hpctm-1459.git"

    version('develop', branch='main', submodules=False)
    version('1.0.20210913', commit='8a5fe64', submodules=False)
    version('1.0.20210902', commit='be8b19d', submodules=False)
    # version('1.0', tag='v1.0', submodules=False)

    depends_on('cmake', type='build')
