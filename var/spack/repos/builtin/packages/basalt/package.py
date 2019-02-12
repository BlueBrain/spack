# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install basalt
#
# You can edit this file again by typing:
#
#     spack edit basalt
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Basalt(PythonPackage):
    """C++11 Graph Storage library"""

    homepage = "https://github.com/tristan0x/basalt"
    url      = "git@github.com:tristan0x/basalt.git"
    
    version('develop', git=url, branch='master', submodules=True, preferred=True)
    version('0.1.1', git=url, tag='v0.1.1', submodules=True)

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('rocksdb~static')
    depends_on('python@3:')
    depends_on('cmake@3.5:')
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('humanize', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('benchmark')
