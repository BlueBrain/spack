# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPandocfilters(PythonPackage):
    """A python module for writing pandoc filters, with a collection of examples"""

    homepage = "https://pypi.org/project/pandocfilters/"
    url      = "https://pypi.io/packages/source/p/pandocfilters/pandocfilters-1.4.2.tar.gz"

    version('1.4.2', 'dc391791ef54c7de1572d7b46b63361f')
