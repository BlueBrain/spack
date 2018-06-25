##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os

from spack import *


class ParquetConverters(CMakePackage):
    """Parquet conversion tools developed by Blue Brain Project, EPFL
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/ParquetConverters"
    url      = "ssh://bbpcode.epfl.ch/building/ParquetConverters"

    version('develop', git=url, preferred=True)

    depends_on('hdf5')
    depends_on('highfive')
    depends_on('parquet')
    depends_on('snappy ~shared')
    depends_on('synapse-tool +mpi')
    depends_on('mpi')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('CC', self.spec['mpi'].mpicc)
        spack_env.set('CXX', self.spec['mpi'].mpicxx)

    def cmake_args(self):
        return ['-DNEURONPARQUET_USE_MPI=ON']
