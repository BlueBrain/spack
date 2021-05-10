# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTns(PythonPackage):
    """Python library for neuron synthesis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/TNS"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/TNS"

    version('develop', branch='master')
    version('space2', branch='space2')
    version('2.4.2', tag='TNS-v2.4.2')
    version('2.3.2', tag='TNS-v2.3.2')
    version('2.2.7', tag='tns-v2.2.7')
    version('2.0.4', tag='tns-v2.0.4')
    version('1.0.8', tag='tns-v1.0.8')

    depends_on('py-setuptools', type='build')

    depends_on('py-matplotlib@1.3:', type='run')
    depends_on('py-morphio@2.7.1:', type='run')
    depends_on('py-neurom@2:2.999', type='run')
    depends_on('py-numpy@1.15.0:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-tmd@2.0.8:', type='run')
    depends_on('py-jsonschema@3.0.1:', type='run')
