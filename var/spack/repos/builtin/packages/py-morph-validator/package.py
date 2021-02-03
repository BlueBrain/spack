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

    depends_on('pandas@0.25:', type='run')
    depends_on('joblib@0.14:', type='run')
    depends_on('numpy@1.14:', type='run')
    depends_on('scipy@1.3:', type='run')
    depends_on('lxml@4.3.4:', type='run')
    depends_on('morph-tool@2.3.0:', type='run')
    depends_on('neurom@1.7.0:', type='run')
    depends_on('bluepy@2.0.0:', type='run')
    depends_on('seaborn@0.10.1:', type='run')
    depends_on('tqdm@4.46.0:', type='run')
    depends_on('matplotlib@2.2.0:', type='run')
