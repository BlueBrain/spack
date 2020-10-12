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
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b daint_deployment

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

spack reindex
#spack module tcl refresh -y --delete-tree
module swap PrgEnv-cray PrgEnv-intel
module load daint-mc
module load intel
module list

export LC_CTYPE=en_US.UTF-8

# PYTHON 2 packages
#spack spec -Il neurodamus-hippocampus+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc
#spack install --keep-stage neurodamus-hippocampus+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc
#spack install --keep-stage neurodamus-neocortex+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc
#spack install --keep-stage neurodamus-mousify+coreneuron %intel ^python@2.7.15 ^synapsetool%gcc

#spack spec -I py-bluepy%gcc ^python@2.7.15
#spack install --dirty --keep-stage -v py-bluepy%gcc ^python@2.7.15
#spack spec -I -l py-bluepyopt%gcc^neuron~binary~mpi ^python@2.7.15 ^py-tornado@4.4.0 ^py-ipykernel@4.5.0 ^py-ipython@5.1.0
#spack install --dirty --keep-stage -v py-bluepyopt%gcc^neuron~binary~mpi ^python@2.7.15
#spack spec -I neuron %intel ^python@2.7.15 ^mpich
#spack install --dirty --keep-stage -v neuron %intel ^python@2.7.15 ^mpich

#spack spec -I neuron~mpi %intel ^python@2.7.15
#spack install --dirty --keep-stage -v neuron~mpi %intel ^python@2.7.15

# PYTHON 3 packages
module load cray-python/3.8.2.1
PYTHON_VERSION='^python@3.8.2.1'

spack spec -Il neurodamus-hippocampus+coreneuron %intel $PYTHON_VERSION ^synapsetool%gcc ^spdlog%gcc
spack install --dirty --keep-stage neurodamus-hippocampus+coreneuron %intel $PYTHON_VERSION ^synapsetool%gcc ^spdlog%gcc
spack install --dirty --keep-stage neurodamus-neocortex+coreneuron %intel $PYTHON_VERSION ^synapsetool%gcc ^spdlog%gcc
spack install --dirty --keep-stage neurodamus-mousify+coreneuron %intel $PYTHON_VERSION ^synapsetool%gcc ^spdlog%gcc

spack spec -Il py-neurodamus%intel $PYTHON_VERSION ^py-scipy%gcc
spack install --dirty --keep-stage py-neurodamus%intel $PYTHON_VERSION ^py-scipy%gcc
##spack spec -I neuron~mpi %intel $PYTHON_VERSION
##spack install --dirty --keep-stage -v neuron~mpi %intel $PYTHON_VERSION
module swap PrgEnv-intel PrgEnv-gnu
spack spec -Il py-bluepy%gcc $PYTHON_VERSION ^cmake@3.15.3 ^py-pandas@0.25.3 ^py-h5py@2.11.0a
spack install --dirty --keep-stage -v py-bluepy%gcc $PYTHON_VERSION ^cmake@3.15.3 ^py-pandas@0.25.3 ^py-h5py@2.11.0a

spack spec -Il py-sonata-network-reduction%gcc $PYTHON_VERSION ^spdlog%gcc ^cmake@3.15.3
spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc $PYTHON_VERSION ^spdlog%gcc ^cmake@3.15.3

spack spec -Il py-bluepyopt%gcc $PYTHON_VERSION ^cmake@3.15.3 ^py-pandas@0.25.3
spack install --dirty --keep-stage py-bluepyopt%gcc $PYTHON_VERSION ^cmake@3.15.3 ^py-pandas@0.25.3

spack spec -Il psp-validation%gcc $PYTHON_VERSION ^cmake@3.15.3 ^py-pandas@0.25.3 ^py-h5py@2.11.0a
spack install --dirty psp-validation%gcc $PYTHON_VERSION ^cmake@3.15.3 ^py-pandas@0.25.3 ^py-h5py@2.11.0a

# Re-generate modules
spack module tcl refresh --delete-tree -y
cd $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl7-haswell
find py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'
find neuro* -type f -print0|xargs -0 sed -i '/module load mpich/d'

ln -s $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl6-haswell $DEPLOYMENT_HOME/modules
#chmod -R ugo-w $DEPLOYMENT_HOME

#cd $BASE_DIR
#rm modules
#ln -s $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl6-haswell modules
