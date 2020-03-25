#!/bin/bash
set -x
set -e

# Deployment directory
BASE_DIR=/apps/hbp/ich002/hbp-spack-deployments
DEPLOYMENT_HOME=$BASE_DIR/softwares/$(date '+%d-%m-%Y')

mkdir -p $DEPLOYMENT_HOME
mkdir -p $DEPLOYMENT_HOME/sources
mkdir -p $DEPLOYMENT_HOME/install

export HOME=$DEPLOYMENT_HOME

# Clone spack repository
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b pr/juelich-update

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

#chmod -R ugo+w $DEPLOYMENT_HOME
# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/cray/
cp $SPACK_ROOT/sysconfig/daint/* $SPACK_ROOT/etc/spack/defaults/cray/

# Directory for deployment
export SOFTS_DIR_PATH=$DEPLOYMENT_HOME/install

module swap PrgEnv-cray PrgEnv-intel
module load daint-mc
# PYTHON 2 packages
#spack spec -Il neurodamus-hippocampus+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc
#spack install --keep-stage neurodamus-hippocampus+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc
#spack install --keep-stage neurodamus-neocortex+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc
#spack install --keep-stage neurodamus-mousify+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc

#spack spec -I py-bluepy%gcc ^python@2.7.15
#spack install --dirty --keep-stage -v py-bluepy%gcc ^python@2.7.15
#spack spec -I -l py-bluepyopt%gcc^neuron~binary~mpi ^python@2.7.15 ^py-tornado@4.4.0 ^py-ipykernel@4.5.0 ^py-ipython@5.1.0
#spack install --dirty --keep-stage -v py-bluepyopt%gcc^neuron~binary~mpi ^python@2.7.15
spack spec -I neuron %intel ^python@2.7.15 ^mpich
spack install --dirty --keep-stage -v neuron %intel ^python@2.7.15 ^mpich

spack spec -I neuron~mpi %intel ^python@2.7.15
spack install --dirty --keep-stage -v neuron~mpi %intel ^python@2.7.15
# PYTHON 3 packages
spack spec -Il neurodamus-hippocampus+coreneuron %intel ^python@3.6.5 ^synapsetool%gcc
spack install --dirty --keep-stage neurodamus-hippocampus+coreneuron %intel ^python@3.6.5 ^synapsetool%gcc
spack install --dirty --keep-stage neurodamus-neocortex+coreneuron %intel ^python@3.6.5 ^synapsetool%gcc
spack install --dirty --keep-stage neurodamus-mousify+coreneuron %intel ^python@3.6.5 ^synapsetool%gcc

spack spec -I neuron~mpi %intel ^python@3.6.5
spack install --dirty --keep-stage -v neuron~mpi %intel ^python@3.6.5

module swap PrgEnv-intel PrgEnv-gnu

spack spec -I py-bluepy%gcc ^python@3.6.5
spack install --dirty --keep-stage -v py-bluepy%gcc ^python@3.6.5

spack spec -Il py-sonata-network-reduction%gcc^neuron~binary~mpi ^python@3.6.5 ^zeromq%intel
spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc^neuron~binary~mpi ^python@3.6.5 ^zeromq%intel

spack spec -Il py-bluepyopt%gcc^neuron~binary~mpi ^python@3.6.5 ^zeromq%intel
spack install --dirty --keep-stage py-bluepyopt%gcc^neuron~binary~mpi ^python@3.6.5 ^zeromq%intel

# Re-generate modules
spack module tcl refresh --delete-tree -y

#ln -s $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl6-haswell $DEPLOYMENT_HOME/modules
#chmod -R ugo-w $DEPLOYMENT_HOME

#cd $BASE_DIR
#rm modules
#ln -s $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl6-haswell modules
