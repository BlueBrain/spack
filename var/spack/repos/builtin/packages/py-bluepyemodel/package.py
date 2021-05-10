# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluePyEModel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/cells/BluePyEModel"
    git      = "ssh://bbpcode.epfl.ch/cells/BluePyEModel"

    version('0.0.3', tag='bluepyemodel-v0.0.3')

    depends_on('py-setuptools', type='build')

    depends_on('py-click@7.0:', type='run')
    depends_on('py-numpy@1.15.0:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-h5py@2.9:', type='run')
    depends_on('py-matplotlib@2.2:', type='run')
    depends_on('py-pandas@0.24:', type='run')
    depends_on('py-efel@3.0.80:', type='run')
    depends_on('py-morph-tool@2.4.4:', type='run')
    depends_on('bluepyopt @ git+http://github.com/BlueBrain/BluePyOpt@CMA_clean#egg=bluepyopt', type='run')
    depends_on('bluepyefe @ git+http://github.com/BlueBrain/BluePyEfe@BPE2#egg=bluepyefe', type='run')
