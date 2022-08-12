# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class ThirdpartyHsl(AutotoolsPackage):
    """This is an autotools-based build system to build and install routines from the
    Harwell Subroutine Library (HSL). This installation of HSL routines is used by some
    other COIN-OR projects, in particular Ipopt.
    """

    homepage = "https://github.com/coin-or-tools/ThirdParty-HSL/"
    url      = "https://github.com/coin-or-tools/ThirdParty-HSL/archive/refs/tags/releases/2.2.1.tar.gz"

    version('2.2.1', sha256='b7651a75638b6a3151e4aaf3237f99f98a891afd983fd2ab027c7392afd872ea')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    variant('blas', default=False, description='Link to external BLAS library')

    depends_on('blas', when='+blas')

    # The tarball will have to be renamed to `coinhsl-${version}.tar.gz` on the mirror,
    # with `${version}` being the one of thirdparty-hsl
    resource(
        name='coinhsl',
        url='file://{0}/coinhsl-archive-2021.05.05.tar.gz'.format(os.getcwd()),
        destination='.',
        sha256='5dca8552c4bd8b549cb24359d20c0ec6863542922587a9ab8265c5f0a0ebd424',
    )

    @run_before('configure')
    def move_coinhsl(self):
        with working_dir(self.build_directory):
            mv = which('mv')
            mv('coinhsl-archive-2021.05.05', 'coinhsl')

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('+blas'):
            args.append('--with-blas={0}'.format(spec['blas'].libs.ld_flags))

        return args

    @property
    def libs(self):
        return find_libraries('libcoinhsl*', root=self.prefix, recursive=True)
