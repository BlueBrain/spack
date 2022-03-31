# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlalign(PythonPackage):
    """Blue Brain multi-modal registration and alignment toolbox."""

    homepage = "https://pypi.org/project/atlalign/"
    pypi = "atlalign/atlalign-0.6.1.tar.gz"

    version('0.6.1', sha256='8e3532987ab284211c3408a47855fb0deb439b93d58d92dce44e95a530846b0a')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-antspyx@0.3.1', type=('build', 'run'))
    depends_on('py-imgaug@:0.2.999', type=('build', 'run'))
    depends_on('py-matplotlib@3.0.3:', type=('build', 'run'))
    depends_on('py-mlflow', type=('build', 'run'))
    depends_on('py-nibabel@2.4.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-seaborn', type=('build', 'run'))
    depends_on('py-scikit-image@0.17.1:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.20.2:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    # Addons need to be in lockstep with TF
    depends_on('py-tensorflow@2.6.0:', type=('build', 'run'))
    depends_on('py-tensorflow-addons', type=('build', 'run'))
