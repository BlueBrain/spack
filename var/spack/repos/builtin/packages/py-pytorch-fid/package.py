# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyPytorchFid(PythonPackage):
    "FID score for PyTorch."

    homepage = "https://pypi.org/project/pytorch-fid/"
    url = "https://files.pythonhosted.org/packages/93/54/49dc21a5ee774af0390813c3cf66af57af0a31ab22ba0c2ac02cdddeb755/pytorch-fid-0.2.0.tar.gz"

    version('0.2.0', sha256='5f3aa23957623fcd0150c467478cdf67b479a2870d570b8c4957d031ac597a11')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('numpy', type('run'))
    depends_on('pillow', type('run'))
    depends_on('scipy', type('run'))
    depends_on('torch@1.0.1:', type('run'))
    depends_on('torchvision@0.2.2:', type('run'))
