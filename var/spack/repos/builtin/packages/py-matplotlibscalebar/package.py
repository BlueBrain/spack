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
#     spack install py-matplotlibscalebar
#
# You can edit this file again by typing:
#
#     spack edit py-matplotlibscalebar
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class PyMatplotlibscalebar(PythonPackage):
    """Provides a new artist for matplotlib to display a scale bar, aka micron bar."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/ppinard/matplotlib-scalebar"
    git      = "https://github.com/ppinard/matplotlib-scalebar.git"

    # FIXME: Add proper versions and checksums here.
    version('develop', git=git, branch='master')
    version('0.6.1', git=git, tag='0.6.1')

    # FIXME: Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-matplotlib', type=('build', 'run'))

