# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDiffeqpy(PythonPackage):
    """Solving differential equations in Python using DifferentialEquations.jl """

    homepage = "http://www.example.com"
    url      = "https://github.com/JuliaDiffEq/diffeqpy/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='227cdd1f5f6608be01d4845d6bd1d400ffa1ab11737dc08c0cdff9c85e0f79bb')

    depends_on('py-setuptools', type='build')
    depends_on('py-julia', type='run')
