# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyNeuror(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/NeuroR"
    git = "https://github.com/BlueBrain/NeuroR.git"
    url = "https://pypi.io/packages/source/n/neuror/neuror-1.1.11.tar.gz"

    version('develop', branch='master')
    version('1.1.11', tag='NeuroR-v1.1.11')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-morph-tool', type='run')
    depends_on('py-pandas@1.0.3:', type='run')
    depends_on('py-pyquaternion@0.9.2:', type='run')
    depends_on('py-plotly-helper', type='run')
    depends_on('py-neurom@mut_morphio', type='run')
    depends_on('py-morphio@2.7.0:', type='run')
