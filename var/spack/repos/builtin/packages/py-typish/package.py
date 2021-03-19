# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyTypish(PythonPackage):
    """Python functions for thorough checks on types."""

    homepage = "https://github.com/ramonhagenaars/typish"
    url = "https://github.com/ramonhagenaars/typish/archive/v1.9.1.tar.gz"

    version('1.9.1', 'd0f8e0dc2161fbe24fba50177e1beaa29d9b811d6374fdcc5af48dd4a5b135db')

    depends_on('py-setuptools', type=('build', 'run'))
