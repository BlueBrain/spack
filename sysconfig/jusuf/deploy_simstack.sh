#!/bin/bash
module --force purge

module load Intel/2019.5.281-GCC-8.3.0 IntelMPI/2019.6.154

set -e
# Deployment directory
#date=$(date '+%d-%m-%Y')
date='10-08-2020'
DEPLOYMENT_HOME=/p/project/cvsk25/software-deployment/HBP/jusuf/$date
mkdir -p $DEPLOYMENT_HOME/sources

# Clone spack repository and setup environment
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/linux/
cp $SPACK_ROOT/sysconfig/jusuf/* $SPACK_ROOT/etc/spack/defaults/linux/

# Directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME
export HOME=/p/project/cvsk25/blancoalonso1/
module list

#spack mirror add local_filesystem /p/project/cvsk25/blancoalonso1/jusuf/mirrors
spack mirror list

# Python 2 packages
#spack spec -Il neuron %intel ^python@2.7.15
#spack install --dirty --keep-stage -v neuron %intel ^python@2.7.15

#spack spec -Il neuron~mpi %intel ^python@2.7.15
#spack install --dirty --keep-stage -v neuron~mpi %intel ^python@2.7.15

# Python 3 packages
module load Python/3.6.8
module load SciPy-Stack/2019a-Python-3.6.8
module list

neurodamus_deps="^coreneuron ^python@3.6.8"
spack spec -Il neurodamus-hippocampus+coreneuron %intel $neurodamus_deps
for nd in neurodamus-hippocampus neurodamus-neocortex neurodamus-mousify
do
   spack install --keep-stage --dirty -v $nd+coreneuron %intel $neurodamus_deps
done

spack spec -Il neuron~mpi %intel ^python@3.6.8
#spack install --dirty --keep-stage -v neuron~mpi %intel ^python@3.6.8

spack spec -Il py-bluepy%gcc ^python@3.6.8
#spack install --dirty --keep-stage -v py-bluepy%gcc ^python@3.6.8

spack spec -Il py-sonata-network-reduction%gcc ^python@3.6.8 ^zeromq%intel
#spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc ^python@3.6.8 ^zeromq%intel

spack spec -Il py-bluepyopt%gcc ^python@3.6.8 ^zeromq%intel
#spack install --keep-stage --dirty -v py-bluepyopt%gcc ^python@3.6.8 ^zeromq%intel

spack module tcl refresh --delete-tree -y
cd $DEPLOYMENT_HOME/modules/tcl/linux-centos7-haswell
find py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'
