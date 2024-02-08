#!/bin/bash
set -x
set -e

# Deployment directory
#date=$(date '+%d-%m-%Y')
date='08-02-2024'

DEPLOYMENT_HOME=/g100_work/icei_H_Ebrait/software-deployment/HBP/$date
mkdir -p $DEPLOYMENT_HOME
mkdir -p $DEPLOYMENT_HOME/sources

# Clone spack repository
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b jblanco/galileo_deployment_2024

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH

# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/linux/
cp $SPACK_ROOT/bluebrain/sysconfig/galileo/* $SPACK_ROOT/etc/spack/defaults/linux/
source $SPACK_ROOT/share/spack/setup-env.sh

# Setup directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME

spack mirror list
#spack mirror rm local_filesystem
#spack mirror add local_filesystem $SPACK_INSTALL_PREFIX/mirrors

# Clean environment and load python
module purge
module load gcc/10.2.0
module load intel/oneapi-2022--binary intelmpi/oneapi-2022--binary
module load python/3.8.12--intel--2021.4.0

spack spec -I neuron~mpi%intel
spack install --dirty --keep-stage neuron~mpi%intel

spack spec -I neurodamus-hippocampus%intel+coreneuron ^py-mvdtool%gcc
spack install --dirty --keep-stage neurodamus-hippocampus%intel+coreneuron ^py-mvdtool%gcc

# python 3 packages
spack spec -Il py-bluepyopt%gcc ^libzmq%intel
spack install --dirty --keep-stage py-bluepyopt%gcc ^libzmq%intel

# matplotlib is external and python3
#spack install --keep-stage --dirty -v py-matplotlib%gcc

spack module tcl refresh -y --delete-tree

# change permissions
#chmod -R g+rx $DEPLOYMENT_HOME
