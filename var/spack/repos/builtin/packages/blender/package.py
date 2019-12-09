# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.

from spack import *

import os
import shutil

class Blender(Package):
    """Blender is the free and open source 3D creation suite."""

    homepage = "https://www.blender.org"
    base_url      = "https://ftp.nluug.nl/pub/graphics/blender/release/"

    version('2.81a-linux-glibc217', sha256='bb6e03ef79d2d7273336f8cfcd5a3b3f', url=base_url+"Blender2.81/blender-2.81a-linux-glibc217-x86_64.tar.bz2")

    def install(self, spec, prefix):
	for file in os.listdir(self.stage.source_path):
            src = os.path.join(self.stage.source_path, file)
            dst = os.path.join(prefix, file)
            if os.path.isdir(src):
                shutil.copytree(src, dst, False)
            else:
                shutil.copy2(src, dst)

    def setup_environment(self, spack_env, run_env):
        blender_python_path = os.path.join(prefix, self.version.string[:4], 'python/lib/python3.7')
        run_env.set('PYTHONPATH', blender_python_path)

