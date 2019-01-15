# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
import os
import shutil


class NeurodamusCore(Package):
    """Library of channels developed by Blue Brain Project, EPFL"""

    homepage = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"
    url      = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"

    version('develop', git=url, branch='master')
    version('2.0.0', tag='2.0.0')

    def install(self, spec, prefix):
        shutil.copytree('hoc', prefix.hoc)
        shutil.copytree('mod', prefix.mod)
        if os.path.isdir('python'):
            shutil.copytree('python', prefix.python)
