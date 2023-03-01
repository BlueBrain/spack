# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIgor2(PythonPackage):
    """igor: interface for reading binary IGOR files."""

    homepage = "http://blog.tremily.us/posts/igor/"
    git = "https://github.com/AFM-analysis/igor2.git"

    version('0.5.2', git=git, tag='0.5.2')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
