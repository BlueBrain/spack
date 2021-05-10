# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRegionGrower(PythonPackage):
    """Python library for space-aware neuron synthesis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/region-grower"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/region-grower"

    version('develop', branch='master')
    version('0.2.1', tag='region-grower-v0.2.1')
    version('0.1.10', tag='region-grower-v0.1.10')
    version('0.1.5', tag='region-grower-v0.1.5')
    version('0.1.2', tag='region-grower-v0.1.2')

    depends_on('py-setuptools', type='build')

    depends_on('py-click@7.0:', type='run')
    depends_on('py-tqdm@4.28.1:', type='run')
    depends_on('py-tns@2.4.0:', type='run')
    depends_on('py-voxcell@2.7:', type='run')
    depends_on('py-diameter-synthesis@0.2.3:', type='run')
    depends_on('py-morphio@2.7:', type='run')
    depends_on('py-neuroc@0.2.3:', type='run')
    depends_on('py-neurom@2:2.999', type='run')
    depends_on('py-morph-tool@2.4.1:', type='run')
    depends_on('py-dask@2.15.0:', type='run')
    depends_on('py-dask-mpi@2.21.0:', type='run', when='+mpi')
    depends_on('py-mpi4py@3.0.3:', type='run', when='+mpi')
    depends_on('py-attrs@19.3.0:', type='run')
