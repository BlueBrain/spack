##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import glob

from spack import *


class OlfactoryBulb3d(Package):
    """Recipe for building olfactory-bulb-3d model special and special-core"""

    homepage = "https://github.com/HumanBrainProject/olfactory-bulb-3d"
    url      = "git@github.com:iomaganaris/olfactory-bulb-3d.git"
    git      = "git@github.com:iomaganaris/olfactory-bulb-3d.git"

    version('develop', branch="master")
    version('0.1.20211014', commit="bd6a76b")

    depends_on('neuron')
    depends_on('coreneuron')

    def install(self, spec, prefix):
        os.mkdir(os.path.join(self.prefix, 'mod'))  
        for modfilename in glob.glob(os.path.join('sim', '*.mod')):
            shutil.copy(modfilename, self.prefix.mod)
        os.chdir(self.prefix)
        which('nrnivmodl')('mod')
        which('nrnivmodl-core')('mod')
        #shutil.copytree('x86_64', self.prefix)
        os.mkdir(os.path.join(self.prefix, 'bin'))
        os.symlink(os.path.join(self.prefix, 'x86_64/special'), os.path.join(self.prefix, 'bin/special'))
        os.symlink(os.path.join(self.prefix, 'x86_64/special-core'), os.path.join(self.prefix, 'bin/special-core'))

