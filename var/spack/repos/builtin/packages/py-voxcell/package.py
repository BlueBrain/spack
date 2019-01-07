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


class PyVoxcell(PythonPackage):
    """Python library for handling volumetric data"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/voxcell"
    git      = "ssh://bbpcode.epfl.ch/nse/voxcell"

    version('develop', branch='master')
    version('2.5.5', tag='voxcell-v2.5.5', preferred=True)

    depends_on('py-setuptools', type='build')

    depends_on('py-future', type='run')
    depends_on('py-h5py~mpi', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-pynrrd', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-six', type='run')
