# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyNptyping(PythonPackage):
    """Type hints for Numpy."""

    homepage = "https://github.com/ramonhagenaars/nptyping"
    url = "https://github.com/ramonhagenaars/nptyping/archive/v1.4.0.tar.gz"

    version('1.4.0', sha256='c20cc20e31fdb4bfade0f129fc144eb01f70ec08d788c8aef21c99643bcc92fd')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-typish@1.7.0:', type='run')
