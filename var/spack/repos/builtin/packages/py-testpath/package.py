# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTestpath(PythonPackage):
    """Test utilities for Python code working with files and commands"""

    homepage = "https://pypi.org/project/testpath/"
    url      = "https://pypi.io/packages/source/t/testpath/testpath-0.4.2.tar.gz"

    version('0.4.2', '562d0e1b02fc5cbcb8406955bcd7249f')
