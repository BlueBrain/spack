# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBbpWorkflow(PythonPackage):
    '''Blue Brain Workflow.'''

    homepage = 'https://bbpgitlab.epfl.ch/nse/bbp-workflow'
    git      = 'git@bbpgitlab.epfl.ch:nse/bbp-workflow.git'

    version('2.1.26', tag='bbp-workflow-v2.1.26')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi',                   type='run')
    depends_on('py-luigi-tools',             type='run')
    depends_on('py-entity-management',       type='run')
    depends_on('py-requests-unixsocket',     type='run')
    depends_on('py-sh',                      type='run')
    depends_on('py-matplotlib',              type='run')
    depends_on('py-dask+diagnostics@2.30.0', type='run')
    depends_on('py-distributed@2.30.1',      type='run')
    depends_on('py-xarray',                  type='run')
    depends_on('py-zarr',                    type='run')
    depends_on('py-notebook',                type='run')
    depends_on('py-ipyparallel',             type='run')

    depends_on('py-docutils', type='run')  # rdflib plugins pull this from python-daemon

    depends_on('py-bluepy',            type='run')
    depends_on('py-bluepy-configfile', type='run')
    depends_on('py-simwriter',         type='run')
    depends_on('py-voxcell',           type='run')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec['py-distributed'].prefix.bin)
        env.prepend_path('PATH', self.spec['py-notebook'].prefix.bin)
        env.prepend_path('PATH', self.spec['py-ipython'].prefix.bin)
        env.prepend_path('PATH', self.spec['py-ipyparallel'].prefix.bin)
        env.prepend_path('PATH', self.spec['py-luigi'].prefix.bin)
