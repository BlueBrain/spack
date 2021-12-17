# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurots(PythonPackage):
    """Python library for neuron synthesis"""

    homepage = "https://github.com/BlueBrain/NeuroTS"
    git      = "git@github.com:BlueBrain/NeuroTS.git"

    version('develop', branch='main')
    version('3.1.0', tag='3.1.0')
    version('3.0.0', tag='3.0.0')
    depends_on("py-setuptools", type="build")

    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-tmd@2.0.8:', type=('build', 'run'))
    depends_on('py-morphio@3.0:3.999', type=('build', 'run'))
    depends_on('py-neurom@3:3.999', type=('build', 'run'))
    depends_on('py-scipy@1.6:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-jsonschema@3.0.1:', type=('build', 'run'))
