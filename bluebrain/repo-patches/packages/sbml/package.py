import os

from spack import *
from spack.pkg.builtin.sbml import Sbml as BuiltinSbml


class Sbml(BuiltinSbml):
    __doc__ = BuiltinSbml.__doc__

    depends_on('py-setuptools', when='+python')
    extends('python', when='+python')

    def cmake_args(self):
        args = super().cmake_args()
        if '+python' in spec:
            args.append(
                '-DPYTHON_INSTALL_WITH_SETUP:BOOL=ON'
            )

    def setup_run_environment(self, env):
        ppath = self.spec['python'].package.site_packages_dir
        if os.path.isdir(self.prefix.lib64):
            ppath = ppath.replace('lib', 'lib64')
        ppath = os.path.join(self.prefix, ppath)
        env.prepend_path('PYTHONPATH', ppath)
