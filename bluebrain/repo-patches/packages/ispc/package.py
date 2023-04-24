# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack.package import *


class Ispc(Package):
    """ispc is a compiler for a variant of the C programming language, with
    extensions for single program, multiple data programming mainly aimed
    at CPU SIMD platforms."""

    homepage = "https://github.com/ispc/ispc/"
    url      = "https://github.com/ispc/ispc/releases/download/v1.10.0/ispc-v1.10.0b-linux.tar.gz"

    version('1.18.0', sha256='6c379bb97962e9de7d24fd48b3f7e647dc42be898e9d187948220268c646b692')
    version('1.16.1', sha256='88db3d0461147c10ed81053a561ec87d3e14265227c03318f4fcaaadc831037f')
    version('1.16.0', sha256='71a20e75ee1b952d8096a842368244111a0a727454d4a42043de10eadf02e740')
    version('1.15.0', sha256='b67f50ab16b38d29e28b0a2dbb9733fd6fc1276cb5a5be0cac78e356941f881f')
    version('1.14.1', sha256='8cc0dae16b3ac244aa05e8b1db1dadf35aeb8d67916aaee6b66efb813b8e9174')
    version('1.13.0', sha256='8ab1189bd5db596b3eee9d9465d3528b6626a7250675d67102761bb0d284cd21')
    version('1.12.0', sha256='7a2bdd5fff5c1882639cfbd66bca31dbb68c7177f3013e80b0813a37fe0fdc23')
    version('1.11.0', sha256='dae7d1abf950dea722fe3c535e4fa43a29c0b67b14d66e566ab2fa760ee82f38')
    version('1.10.0', sha256='453211ade91c33826f4facb1336114831adbd35196d016e09d589a6ad8699aa3')

    def url_for_version(self, version):
        url = "https://github.com/ispc/ispc/releases/download/v{0}/ispc-v{0}{2}-{1}.tar.gz"

        if self.spec.satisfies('@1.13.0:'):
            suffix = ''
        else:
            suffix = 'b'
        return url.format(version, 'linux', suffix)

    def install(self, spec, prefix):
        for d in ['bin', 'examples']:
            if os.path.isdir(d):
                install_tree(d, join_path(self.prefix, d))
