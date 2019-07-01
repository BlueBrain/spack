# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Bbptestdata(CMakePackage):
    """Blue Brain Project scientific test data"""
    git = "ssh://bbpcode.epfl.ch/common/TestData"

    version('2.0.0')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('install')
