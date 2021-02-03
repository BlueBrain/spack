# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMorphValidator(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/morph-validator"
    git      = "ssh://bbpcode.epfl.ch/nse/morph-validator"
    version('develop', branch='master')
    version('0.2.2', tag='morph-validator-v0.2.2')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('pandas', type='run')
    depends_on('joblib', type='run')
    depends_on('numpy', type='run')
    depends_on('scipy', type='run')
    depends_on('lxml', type='run')
    depends_on('morph-tool', type='run')
    depends_on('neurom', type='run')
    depends_on('bluepy', type='run')
    depends_on('seaborn', type='run')
    depends_on('tqdm', type='run')
    depends_on('matplotlib', type='run')
