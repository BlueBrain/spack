# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/morph-tool"
    git      = "https://github.com/BlueBrain/morph-tool.git"
    url      = "https://pypi.io/packages/source/m/morph-tool/morph-tool-2.4.1.tar.gz"

    version('develop', branch='master')
    version('2.9.0', sha256='c60d4010e17ddcc3f53c864c374fffee05713c8f8fd2ba4eed7706041ce1fa47')
    version('2.8.0', sha256='3676d200e30313afee60ba7e232edb76ffa2f3926211eb251df63ffedae96a57')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.7:', type='run')
    depends_on('py-deprecation@2.1.0:', type='run')
    depends_on('py-more-itertools@8.6.0:', type='run')
    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-pandas@1.0.3:', type='run')
    depends_on('py-xmltodict@0.12:', type='run')

    depends_on('py-plotly@4.1:', type='run')
    depends_on('py-dask+bag@2.19:', type='run')
    depends_on('neuron+python@7.8:', type='run')
    depends_on('py-bluepyopt@1.9.37:', type='run')

    depends_on('py-neurom@3.0:3.999', type='run', when='@2.9.0:')
    depends_on('py-neurom@2.0:2.999', type='run', when='@:2.8.99')
    depends_on('py-morphio@3.0:3.999', type='run')
