import os
import shlex

from spack import *
from spack.pkg.builtin.sbml import Sbml as BuiltinSbml


class Sbml(BuiltinSbml):
    __doc__ = BuiltinSbml.__doc__

    depends_on('py-setuptools', type='build', when='+python')
    extends('python', when='+python')

    def cmake_args(self):
        args = super().cmake_args()
        if '+python' in self.spec:
            args.extend([
                '-DPYTHON_INSTALL_IN_PREFIX:BOOL=OFF',
                '-DPYTHON_INSTALL_WITH_SETUP:BOOL=ON',
            ])
        return args

    def patch(self):
        if self.spec.satisfies('+python'):
            args = shlex.join(
                self.spec['py-setuptools'].package.install_args(
                    self.spec,
                    self.prefix
                )
            )
            filter_file(
                'setup.py install',
                'setup.py install {0}'.format(args),
                'src/bindings/python/CMakeLists.txt'
            )
