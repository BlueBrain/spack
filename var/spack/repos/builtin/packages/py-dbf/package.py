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


class PyDbf(PythonPackage):
    """Pure python package for reading/writing dBase, FoxPro, and Visual FoxPro
    .dbf files (including memos)"""

    homepage = 'https://pypi.python.org/pypi/dbf'
    url      = "https://pypi.io/packages/source/d/dbf/dbf-0.96.005.tar.gz"

    version('0.97.11', sha256='8aa5a73d8b140aa3c511a3b5b204a67d391962e90c66b380dd048fcae6ddbb68')
    version('0.96.005', 'bce1a1ed8b454a30606e7e18dd2f8277')
    version('0.94.003', '33a659ec90d7e8d8ffcd69d2189c0c6c')
