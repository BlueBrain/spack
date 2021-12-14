##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import glob

from spack import *


class NetpyneMOne(Package):
    """Recipe for building netpyne M1 model special and special-core"""

    homepage = "https://github.com/suny-downstate-medical-center/M1"
    url      = "git@github.com:iomaganaris/M1.git"
    git      = "git@github.com:iomaganaris/M1.git"

    version('0.1-20211206', git=git, commit='e015dc6fe44387dad4aa22ce14f2d86a15453e40')
    version('0.1-20211124', git=git, commit='a33587a782fa139f371ced7cc78b1f2799f72dec')

    depends_on('py-netpyne', type=('run'))
    depends_on('neuron')
    depends_on('coreneuron')

    def install(self, spec, prefix):
        shutil.copytree(os.path.join('mod'), os.path.join(self.prefix, 'mod'))    
        os.chdir(self.prefix)
        which('nrnivmodl')('mod')
        which('nrnivmodl-core')('mod')
        os.mkdir(os.path.join(self.prefix, 'bin'))
        os.symlink(os.path.join(self.prefix, 'x86_64/special'), os.path.join(self.prefix, 'bin/special'))
        os.symlink(os.path.join(self.prefix, 'x86_64/special-core'), os.path.join(self.prefix, 'bin/special-core'))

