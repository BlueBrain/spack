import os

from spack import *
from spack.pkg.builtin.sbml import Sbml as BuiltinSbml


class Sbml(BuiltinSbml):
    __doc__ = BuiltinSbml.__doc__

    extends('python', when='+python')

    def setup_run_environment(self, env):
        ppath = self.spec['python'].package.site_packages_dir
        if os.path.isdir(self.prefix.lib64):
            ppath = ppath.replace('lib', 'lib64')
        # This package nests one level deeper than expected via a .pth file
        ppath = os.path.join(self.prefix, ppath, 'libsbml')
        env.prepend_path('PYTHONPATH', ppath)
