import os
from spack import *
from spack.pkg.builtin.sbml import Sbml as BuiltinSbml


class Sbml(BuiltinSbml):
    __doc__ = BuiltinSbml.__doc__

    extends('python', when='+python')

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib64):
            ppath = self.spec['python'].site_packages_dir
            ppath = ppath.replace('lib', 'lib64')
            ppath = os.path.join(ppath, 'libsbml')
            env.prepend_path('PYTHONPATH', ppath)
