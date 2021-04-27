# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlasAnalysis(PythonPackage):
    """Python library for brain atlas analyses"""
    homepage = "https://bbpcode.epfl.ch/browse/code/nse/atlas-analysis/tree/"
    git      = "ssh://bbpcode.epfl.ch/nse/atlas-analysis"

    version('0.0.3', tag='atlas-analysis-v0.0.3')

    depends_on('py-setuptools', type='build')
    depends_on('py-click@7.0:', type='run')
    #depends_on('py-geomdl@5.2.8:', type='run')
    depends_on('py-lazy@1.16.3:', type='run')
    depends_on('py-networkx@2.3:', type='run')
    depends_on('py-numpy@1.16.3:', type='run')
    depends_on('py-pathos@0.2.3:', type='run')
    depends_on('py-plotly-helper@0.0.2:', type='run')
    depends_on('py-pyquaternion@0.9.5:', type='run')
    depends_on('py-scipy@1.2.1:', type='run')
    depends_on('py-voxcell@2.6.2:', type='run')
    #depends_on('py-vtk@8.1.2:', type='run')
    depends_on('vtk@8.1.2:', type='run')
    depends_on('py-six@1.12.0:', type='run')
    depends_on('py-scikit-image@0.16.1', type='run')
