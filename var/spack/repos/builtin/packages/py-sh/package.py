# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySh(PythonPackage):
    """Python subprocess interface"""

    homepage = "https://github.com/amoffat/sh"
    pypi = "sh/sh-1.12.9.tar.gz"

    version('1.13.1', sha256='97a3d2205e3c6a842d87ebbc9ae93acae5a352b1bc4609b428d0fd5bb9e286a3')
    version('1.12.9', sha256='579aa19bae7fe86b607df1afaf4e8537c453d2ce3d84e1d3957e099359a51677')
    version('1.11',   sha256='590fb9b84abf8b1f560df92d73d87965f1e85c6b8330f8a5f6b336b36f0559a4')

    depends_on('py-setuptools', type='build')
