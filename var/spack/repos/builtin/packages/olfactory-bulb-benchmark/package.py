# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install olfactory-bulb-benchmark
#
# You can edit this file again by typing:
#
#     spack edit olfactory-bulb-benchmark
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
import shutil
import glob

from spack import *


class OlfactoryBulbBenchmark(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "git@github.com:iomaganaris/olfactory-bulb-3d.git"
    url      = "git@github.com:iomaganaris/olfactory-bulb-3d.git"
    git      = "git@github.com:iomaganaris/olfactory-bulb-3d.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    version('develop', branch="master")
    version('benchmark', branch="2to3_bench")

    variant('gpu', default=False, description="Enable GPU execution")
    variant('nmodl', default=False, description="Enable NMODL translator")
    variant('sympy', default=False, description="Enable sympy solver with NMODL translator")

    depends_on('neuron@develop~legacy-unit~rx3d%intel')
    depends_on('coreneuron@develop~gpu~nmodl~sympy%intel', when='~gpu~nmodl~sympy')
    depends_on('coreneuron@develop~gpu+nmodl~sympy%intel ^nmodl@develop%gcc', when='+nmodl')
    depends_on('coreneuron@develop~gpu+nmodl+sympy%intel ^nmodl@develop%gcc', when='+nmodl+sympy')
    depends_on('coreneuron@develop+gpu~nmodl~sympy%nvhpc@21.2 ^nmodl@develop%gcc', when='+gpu')
    depends_on('coreneuron@develop+gpu+nmodl~sympy%nvhpc@21.2 ^nmodl@develop%gcc', when='+gpu+nmodl')
    depends_on('coreneuron@develop+gpu+nmodl+sympy%nvhpc@21.2 ^nmodl@develop%gcc', when='+gpu+nmodl+sympy')
    conflicts('+sympy', when='~nmodl')

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

