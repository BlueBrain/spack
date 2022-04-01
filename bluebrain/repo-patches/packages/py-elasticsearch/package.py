# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.py_elasticsearch import PyElasticSearch as BuiltinPyElasticSearch


class PyElasticSearch(BuiltinPyElasticSearch):
    __doc__ = BuiltinPyElasticSearch.__doc__

    version('7.6.0', sha256='d228b2d37ac0865f7631335268172dbdaa426adec1da3ed006dddf05134f89c8')

    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.8:1', type=('build', 'run'))
