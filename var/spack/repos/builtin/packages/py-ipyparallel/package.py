##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyIpyparallel(PythonPackage):
    """Use multiple instances of IPython in parallel, interactively."""

    homepage = "http://ipython.org"
    url = "https://pypi.io/packages/source/i/ipyparallel/ipyparallel-6.3.0.tar.gz"

    version('6.3.0', sha256='0a97b276c62db633e9e97a816282bdd166f9df74e28204f0c8fa54b71944cfdc')

    depends_on('py-setuptools', type='build')
    depends_on('py-tornado', type='run')
    depends_on('py-traitlets', type='run')
    depends_on('py-decorator', type='run')
    depends_on('py-pyzmq', type='run')
    depends_on('py-ipython-genutils', type='run')
    depends_on('py-ipython', type='run')
    depends_on('py-ipykernel', type='run')
    depends_on('py-jupyter-client', type='run')
    depends_on('py-python-dateutil', type='run')
