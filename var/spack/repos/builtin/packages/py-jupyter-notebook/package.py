# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterNotebook(PythonPackage):
    """Jupyter Interactive Notebook"""

    homepage = "https://github.com/jupyter/notebook"
    url      = "https://github.com/jupyter/notebook/archive/6.0.0.tar.gz"

    version('6.0.0', 'c4b8ab96014301dd242a8bc0dd86b853')

    variant('terminal', default=False, description="Enable terminal functionality")

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('python@2.7:2.8,3.3:')
    depends_on('npm', type='build')
    depends_on('node-js', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-tornado@6:', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-jupyter-console', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-nbconvert', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-ipykernel@:4.999', type=('build', 'run'), when='^python@:2.7')
    depends_on('py-zmq', type=('build', 'run'))
    depends_on('py-prometheus-client', type=('build', 'run'))
    depends_on('py-send2trash', type=('build', 'run'))
    depends_on('py-terminado@0.3.3:', when="+terminal", type=('build', 'run'))
    depends_on('py-ipywidgets', when="+terminal", type=('build', 'run'))
