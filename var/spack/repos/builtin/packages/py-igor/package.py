# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIgor(PythonPackage):
    """igor: interface for reading binary IGOR files."""

    homepage = "http://blog.tremily.us/posts/igor/"
    url = "https://pypi.io/packages/source/i/igor/igor-0.3.tar.gz"

    version('0.3', branch='master')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type='run')
    depends_on('py-nose', type='run')
    depends_on('py-matplotlib', type='run')

