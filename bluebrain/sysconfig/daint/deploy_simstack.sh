#!/bin/bash
set -x
set -e

# Deployment directory
#BASE_DIR=/scratch/snx3000/bp000271
BASE_DIR=/apps/hbp/ich002/hbp-spack-deployments
DEPLOYMENT_HOME=$BASE_DIR/softwares/23-02-2022
MIRROR_PATH=$DEPLOYMENT_HOME/mirrors

mkdir -p $DEPLOYMENT_HOME
mkdir -p $DEPLOYMENT_HOME/sources
mkdir -p $DEPLOYMENT_HOME/install

export HOME=$DEPLOYMENT_HOME

# Clone spack repository
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b new_daint_deployment

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

#chmod -R ugo+w $DEPLOYMENT_HOME
# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/cray/
cp $SPACK_ROOT/bluebrain/sysconfig/daint/* $SPACK_ROOT/etc/spack/defaults/cray/

# Directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME

spack mirror list
# DO ONLY ONCE
spack mirror remove local_filesystem
spack mirror add local_filesystem $MIRROR_PATH

# create environment
# DO ONLY ONCE
#spack env create myenv
spack env activate myenv

module swap PrgEnv-cray PrgEnv-intel
module load daint-mc
module load intel/19.0.1.144
module list

export LC_CTYPE=en_US.UTF-8

# PYTHON 3 packages
module load cray-python/3.9.4.1
PYTHON_VERSION='^python@3.9.4.1'
spack spec -Il neurodamus-hippocampus+coreneuron %intel $PYTHON_VERSION
spack install --dirty --keep-stage neurodamus-hippocampus+coreneuron %intel $PYTHON_VERSION
spack install --dirty --keep-stage neurodamus-neocortex+coreneuron %intel $PYTHON_VERSION
spack install --dirty --keep-stage neurodamus-mousify+coreneuron %intel $PYTHON_VERSION

# Add packages to myenv that are not explicity installed
#spack add py-neurodamus
#spack add py-libsonata
#spack add neuron

#spack spec -Il py-neurodamus%intel $PYTHON_VERSION
#spack install --dirty --keep-stage py-neurodamus%intel $PYTHON_VERSION

#spack spec -Il py-libsonata%intel $PYTHON_VERSION
#spack install --dirty --keep-stage py-libsonata%intel $PYTHON_VERSION

#spack spec -Il neuron@8.0.2%intel
#spack install --dirty --keep-stage neuron@8.0.2%intel

module swap PrgEnv-intel PrgEnv-gnu
module load gcc
module list

spack spec -Il py-bluepy%gcc $PYTHON_VERSION
spack install --dirty --keep-stage -v py-bluepy%gcc $PYTHON_VERSION

spack spec -Il py-sonata-network-reduction%gcc $PYTHON_VERSION ^libzmq%intel
spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc $PYTHON_VERSION ^libzmq%intel

spack spec -Il py-bluepyopt%gcc $PYTHON_VERSION ^libzmq%intel
spack install --dirty --keep-stage py-bluepyopt%gcc $PYTHON_VERSION ^libzmq%intel

spack spec -Il psp-validation%gcc $PYTHON_VERSION
spack install --dirty psp-validation%gcc $PYTHON_VERSION

spack spec -Il emsim%gcc $PYTHON_VERSION
spack install --dirty emsim%gcc $PYTHON_VERSION

spack spec -Il py-netpyne%gcc $PYTHON_VERSION
spack install -v --dirty --keep-stage py-netpyne%gcc $PYTHON_VERSION

spack concretize -f
spack python $DEPLOYMENT_HOME/hashes.py | tee $DEPLOYMENT_HOME/specs.txt
cat $DEPLOYMENT_HOME/specs.txt

shas="$(cut -d" " -f1 $DEPLOYMENT_HOME/specs.txt)"

# Re-generate modules
spack module tcl refresh --delete-tree -y ${shas}
cd $DEPLOYMENT_HOME/modules/tcl/cray-cnl7-haswell
find py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'
find py* -type f -print0|xargs -0 sed -i 's/mpich/cray-mpich/g'
find neuro* -type f -print0|xargs -0 sed -i '/module load mpich/d'

