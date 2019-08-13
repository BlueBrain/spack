# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWebencodings(PythonPackage):
    """Character encoding for the web"""

    homepage = "https://pypi.org/project/webencodings/"
    url      = "https://pypi.io/packages/source/w/webencodings/webencodings-0.5.1.tar.gz"

    version('0.5.1', '32f6e261d52e57bf7e1c4d41546d15b8')

    depends_on('py-setuptools', type='build')
