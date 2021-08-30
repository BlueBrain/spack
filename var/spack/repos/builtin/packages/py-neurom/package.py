# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurom(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://github.com/BlueBrain/NeuroM"
    git = "https://github.com/BlueBrain/NeuroM.git"
    url = "https://pypi.io/packages/source/n/neurom/neurom-2.2.1.tar.gz"

    version('develop', branch='master')
    version('3.0.0',  sha256='05f5f5c4292dfa23f3319347cf2a7c147732ba0140b9db0bc94e535ac74be8da')
    version('2.3.1',  sha256='d399b2ff22b4dfc1d9ac0f28be49d631a7a48a3fe0b9f13cb880ff60d0a1beba')
    version('2.2.1',  sha256='72f6a552b53ced520a3ccb1a2986ff95ff91df99d9227213f671f87a8d8b6499')
    version('2.1.2',  sha256='6ca24ce628cfa00ba63bc3bd362e9ad1cd337a4ad4d02a5a58ed82ec8e61ce97')
    version('1.8.0',  sha256='d364d3b184bd96cbe5fa601ae24f6b7d431fa42de646e3011a33d56f3cfc247c')
    version('1.7.0',  sha256='713d874538f1c566b57ab81e0558726fc6d4b7de91301a6be495776c55ac47f8')
    version('1.6.0',  sha256='74759199c5392ae8e209f037a5046646d06ec1f77b1cd826afac71eeeca0f7ab')
    version('1.5.0',  sha256='40a4362b58cbbbac769a1cef5b6e5e6ececbf4b538d81c0ed23fe421645aa3c4')

    variant('plotly', default=False, description="Enable plotly support")

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-click@7.0:', type='run')
    depends_on('py-numpy@1.8.0:', type='run')
    depends_on('py-pyyaml@3.10:', type='run')
    depends_on('py-tqdm@4.8.4:', type='run')
    depends_on('py-matplotlib@3.2.1:', type='run')
    depends_on('py-scipy@1.2.0:', type='run')
    depends_on('py-plotly@3.6.0:', type='run', when='+plotly')

    depends_on('py-morphio@3.1.1:', type='run', when='@2.0:')
    depends_on('py-pandas@1.0.5:', type='run', when='@1.6:')
    depends_on('py-h5py@3.1.0:', type='run', when='@1.6:1.999')
    depends_on('py-h5py@2.7.1:2.999', type='run', when='@:1.5.999')
