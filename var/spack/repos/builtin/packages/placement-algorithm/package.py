# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PlacementAlgorithm(PythonPackage):
    """Morphology placement algorithm"""

    homepage = "https://bbpgitlab.epfl.ch/nse/placement-algorithm/"
    git      = "git@bbpgitlab.epfl.ch:nse/placement-algorithm.git"

    version('develop', branch='master')
    version('2.1.2', tag='placement-algorithm-v2.1.2')
    version('2.1.1', tag='placement-algorithm-v2.1.1')
    version('2.1.0', tag='placement-algorithm-v2.1.0')
    version('2.0.10', tag='placement-algorithm-v2.0.10')
    version('2.0.8', tag='placement-algorithm-v2.0.8')

    build_directory = 'python'

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-lxml', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-six', type='run')

    depends_on('py-morphio@2.0.5:', type='run')
    depends_on('py-morph-tool@0.1.3:2.8.99', type='run')
    depends_on('py-neurom@:2.99', type='run')
    depends_on('py-mpi4py@2.0:', type='run')
    depends_on('py-tqdm@4.0:', type='run')
    depends_on('py-voxcell@2.5:2.6.99', when='@:2.0.99', type='run')
    depends_on('py-voxcell@2.7:', when='@2.1.0:', type='run')
    depends_on('py-dask@2.15:', when='@2.0.12:', type='run')

    depends_on('py-region-grower@0.1.5:', type='run')
