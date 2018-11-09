##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
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

from spack import *


class Libsonata(CMakePackage):
    """
    `libsonata` provides C++ / Python API for reading SONATA Nodes / Edges

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/common/libsonata"
    url      = "ssh://bbpcode.epfl.ch/common/libsonata"

    version('dev', git=url, submodules=True)

    variant('mpi', default=False, description="Enable MPI backend")

    depends_on('cmake@3.0:', type='build')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    # TODO: depends_on('python')

    patch('CMakeLists.patch')  # remove '-pedantic' compiler option (it's not happy with MPI headers)

    def cmake_args(self):
        result = [
            # TODO: '-DSONATA_PYTHON=ON',
        ]
        if self.spec.satisfies('+mpi'):
            result.extend([
                '-DCMAKE_C_COMPILER:STRING={}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={}'.format(self.spec['mpi'].mpicxx),
            ])
        return result
