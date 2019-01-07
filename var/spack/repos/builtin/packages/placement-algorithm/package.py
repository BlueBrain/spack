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


class PlacementAlgorithm(PythonPackage):
    """Morphology placement algorithm"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/placementAlgorithm"
    git      = "ssh://bbpcode.epfl.ch/building/placementAlgorithm"

    version('develop', branch='master')
    version('2.0.0', tag='placement-algorithm-v2.0.0', preferred=True)

    variant('app', default=False, description='Applications')
    variant('synthesis', default=False, description='Morphology synthesis')

    build_directory = 'python'

    depends_on('py-setuptools', type='build')

    depends_on('py-lxml', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-six', type='run')

    depends_on('py-morphio', type='run', when='+app')
    depends_on('py-morph-tool', type='run', when='+app')
    depends_on('py-mpi4py', type='run', when='+app')
    depends_on('py-tqdm', type='run', when='+app')
    depends_on('py-ujson', type='run', when='+app')
    depends_on('py-voxcell', type='run', when='+app')
