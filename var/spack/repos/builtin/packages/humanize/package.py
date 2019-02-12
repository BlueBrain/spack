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
#     spack install humanize
#
# You can edit this file again by typing:
#
#     spack edit humanize
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Humanize(PythonPackage):
    """Python package that contains humanization utilities"""

    homepage = "https://github.com/jmoiron/humanize"
    url      = "git@github.com:jmoiron/humanize.git"

    # FIXME: Add proper versions and checksums here.
    version('develop', git=url, branch='master')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    #def install(self, spec, prefix):
    #    # FIXME: Unknown build system
    #    make()
    #    make('install')
    depends_on('py-setuptools', type=('build', 'run'))
