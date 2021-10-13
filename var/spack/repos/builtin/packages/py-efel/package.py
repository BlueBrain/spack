##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyEfel(PythonPackage):
    """The Electrophys Feature Extract Library (eFEL) allows
    neuroscientists to automatically extract features from time series data
    recorded from neurons (both in vitro and in silico).
    Examples are the action potential width and amplitude in
    voltage traces recorded during whole-cell patch clamp experiments.
    The user of the library provides a set of traces and selects the
    features to be calculated. The library will then extract the requested
    features and return the values to the user."""
    homepage = "https://github.com/BlueBrain/eFEL"
    url = "https://pypi.io/packages/source/e/efel/efel-3.0.80.tar.gz"

    version('4.0.4', sha256='258c506776df609edc799338fd773e78f0f0315fd6f3e2f969478bda401a8894')
    version('3.0.80', sha256='daad2a0fd98643e649f8556412b25502c35294ca8435625f87fb1de9bb060e08')
    version('3.0.70', sha256='3f3368012cdec5ca7d5551cea35b30a53befd0c0c740fc535209f840616c07b1')
    version('3.0.22', sha256='97b2c1a0425b12cd419e8539bb1e936ce64c4e93f5d0dd7f81f38554490064a2')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type='run')
    depends_on('py-six', type='run')
