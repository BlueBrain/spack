# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import platform

class JuliaDev(Package):
    """Meta package to bundle julia packages for development"""

    homepage = "http://www.dummy.org/"
    url      = "https://www.dummy.org/source/dummy-0.1.zip"

    version('0.1')

    depends_on('julia', type=('build', 'run'))
    depends_on('py-diffeqpy', type=('build', 'run'))
    depends_on('py-julia', type=('build', 'run'))

    def do_stage(self, mirror_only=False):
        build_dir = os.path.join(self.stage.path, 'build')
        os.makedirs(build_dir)

    def install(self, spec, prefix):
        open(os.path.join(prefix, 'success.txt'), 'w').close()

    def setup_environment(self, spack_env, run_env):
        deps = ['julia']
        for dep in deps:
            run_env.prepend_path('PATH', self.spec[dep].prefix.bin)
