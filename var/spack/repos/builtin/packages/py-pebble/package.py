# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPebble(PythonPackage):
    """PyUnit-based test runner with JUnit like XML reporting."""

    homepage = "https://github.com/noxdafox/pebble"
    url = "https://github.com/noxdafox/pebble/archive/4.5.0.tar.gz"
    git = "git@github.com:noxdafox/pebble.git"

    version('4.3.9', tag='4.3.9')
    version('4.3.10', tag='4.3.10')
    version('4.4.0', tag='4.4.0')
    version('4.5.0', tag='4.5.0')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-futures', type='run', when='^python@:2.9.9')
