# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDefusedxml(PythonPackage):
    """XML bomb protection for Python stdlib modules"""

    homepage = "https://pypi.org/project/defusedxml/"
    url      = "https://pypi.io/packages/source/d/defusedxml/defusedxml-0.6.0.tar.gz"

    version('0.6.0', 'a59741f675c4cba649de40a99f732897')

    depends_on('py-setuptools', type='build')
