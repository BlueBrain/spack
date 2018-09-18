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


class OmegaH(CMakePackage):
    """Omega_h is a C++11 library providing data structures and algorithms
    for adaptive discretizations. Its specialty is anisotropic triangle and
    tetrahedral mesh adaptation. It runs efficiently on most modern HPC
    hardware including GPUs.
    """

    homepage = "https://github.com/ibaned/omega_h"
    url      = "https://github.com/ibaned/omega_h/archive/v9.13.4.tar.gz"
    git      = "https://github.com/ibaned/omega_h.git"

    version('develop', branch='master')
    version('9.17.2', sha256='d9399a23b4f717be836e736090017e9250b944e306bd41286bc6dec02d2e72e3')
    version('9.17.1', sha256='7337b4f900cdcca5019aaf63a3dce80f544e42d7604dc06f4c52cb6d2df5866f')
    version('9.17.0', sha256='3cd19b0502ca90d1091bba0b587abab1e7455dea3deb51f732df8705688b49b4')
    version('9.16.0', sha256='4f318782258dea20df06aab3ac488d86283a189576202025624057e73d09b307')

    variant('shared', default=True, description='Build shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('zlib', default=True, description='Activates ZLib support')
    variant('trilinos', default=True, description='Use Teuchos and Kokkos')
    variant('build_type', default='')
    variant('gmodel', default=True, description='Gmsh model generation library')
    variant('throw', default=False, description='Errors throw exceptions instead of abort')
    variant('examples', default=False, description='Compile examples')
    variant('optimize', default=True, description='Compile C++ with optimization')
    variant('symbols', default=True, description='Compile C++ with debug symbols')
    variant('warnings', default=True, description='Compile C++ with warnings')

    depends_on('gmodel', when='+gmodel')
    depends_on('gmsh', when='+examples', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos +kokkos +teuchos', when='+trilinos')
    depends_on('zlib', when='+zlib')

    def _bob_options(self):
        cmake_var_prefix = self.name.capitalize() + '_CXX_'
        for variant in ['optimize', 'symbols', 'warnings']:
            cmake_var = cmake_var_prefix + variant.upper()
            if '+' + variant in self.spec:
                yield '-D' + cmake_var + ':BOOL=ON'
            else:
                yield '-D' + cmake_var + ':BOOL=FALSE'

    def cmake_args(self):
        args = ['-DUSE_XSDK_DEFAULTS:BOOL=OFF']
        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
        if '+mpi' in self.spec:
            args.append('-DOmega_h_USE_MPI:BOOL=ON')
            args.append('-DCMAKE_CXX_COMPILER:FILEPATH={0}'.format(
                self.spec['mpi'].mpicxx))
        else:
            args.append('-DOmega_h_USE_MPI:BOOL=OFF')
        if '+trilinos' in self.spec:
            args.append('-DOmega_h_USE_Trilinos:BOOL=ON')
        if '+gmodel' in self.spec:
            args.append('-DOmega_h_USE_Gmodel:BOOL=ON')
        if '+zlib' in self.spec:
            args.append('-DTPL_ENABLE_ZLIB:BOOL=ON')
            args.append('-DTPL_ZLIB_INCLUDE_DIRS:STRING={0}'.format(
                self.spec['zlib'].prefix.include))
            args.append('-DTPL_ZLIB_LIBRARIES:STRING={0}'.format(
                self.spec['zlib'].libs))
        else:
            args.append('-DTPL_ENABLE_ZLIB:BOOL=OFF')
        if '+examples' in self.spec:
            args.append('-DOmega_h_EXAMPLES:BOOL=ON')
        else:
            args.append('-DOmega_h_EXAMPLES:BOOL=OFF')
        if '+throw' in self.spec:
            args.append('-DOmega_h_THROW:BOOL=ON')
        else:
            args.append('-DOmega_h_THROW:BOOL=OFF')
        args += list(self._bob_options())
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
