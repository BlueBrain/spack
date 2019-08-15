# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpyparallel(PythonPackage):
    """Use multiple instances of IPython in parallel, interactively."""

    homepage = "http://ipython.org"
    url = "https://pypi.io/packages/source/i/ipyparallel/ipyparallel-6.2.2.tar.gz"

    version('6.2.4', sha256='76c7b028962b0ba762e4e45b450ee3a4353e7221526a8af812e817d7ef6ac065')
    version('6.2.2', sha256='02b225966d5c20f12b1fba0b6b10aa5d352a6b492e075f137ff0ff6e95b9358e')

    depends_on('py-setuptools', type='build')
    depends_on('py-tornado', type='run')
    depends_on('py-traitlets', type='run')
    depends_on('py-zmq', type='run')
    depends_on('py-zmq@:16', type='run', when='^python@:2.7')
    depends_on('py-ipython', type='run')
    depends_on('py-ipython@:6.999', type='run', when='^python@:2.7')
    depends_on('py-ipykernel', type='run')
    depends_on('py-ipykernel@:4.999', type='run', when='^python@:2.7')
    depends_on('py-futures', type='run', when='^python@:2.7')
