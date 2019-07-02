# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJulia(PythonPackage):
    """Python interface to Julia"""

    homepage = "https://github.com/JuliaPy/pyjulia"
    url      = "https://github.com/JuliaPy/pyjulia/archive/v0.4.1.tar.gz"

    version('0.4.1', sha256='14d2b2cf98fd9ede6f12de45477d059ef30d7f3bdc749e53313790db5a5d1862')

    depends_on('py-setuptools', type='build')
    depends_on('julia+python', type='run')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path("PATH", self.spec["julia"].prefix.bin)
