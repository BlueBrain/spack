# Copyright 2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPyquaternion(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://kieranwynn.github.io/pyquaternion/"
    url      = "https://files.pythonhosted.org/packages/ae/c8/02b30c4a86744d2e15f7f16ab353f7231bd0241117713e5d60f466044994/pyquaternion-0.9.5.tar.gz"

    version('0.9.5', sha256='2d89d19259d62a8fbd25219eee7dacc1f6bb570becb70e1e883f622597c7d81d')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy', type='run')
