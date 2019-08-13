# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBleach(PythonPackage):
    """An easy whitelist-based HTML-sanitizing tool."""

    homepage = "http://github.com/mozilla/bleach"
    url      = "https://pypi.io/packages/source/b/bleach/bleach-1.5.0.tar.gz"

    version('3.1.0', 'fc8df989e0200a45f7a3a95ef9ee9854')
    version('1.5.0', 'b663300efdf421b3b727b19d7be9c7e7')

    depends_on('python@3.6:', when='@3:')
    depends_on('py-webencodings', type=('run'), when='@3:')

    depends_on('python@2.6:2.8,3.2:3.5', when='@:2')
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-html5lib@0.999,0.999999:0.9999999', type=('build', 'run'), when='@:2')
