#!/bin/bash
module --force purge

rm -rf ~/.spack/
module load Stages/2024
module load Intel/2023.2.1 ParaStationMPI/5.9.2-1
#module load HDF5/1.12.1
module load Python/3.11.3

#set -e
# Deployment directory
#date=$(date '+%d-%m-%Y')
project='icei-hbp-2020-0013'
date='03-04-2024'
DEPLOYMENT_HOME=/p/project/$project/software-deployment/HBP/jusuf/$date
mkdir -p $DEPLOYMENT_HOME/sources

# Clone spack repository and setup environment
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b jblanco/jusuf_deployment_2024

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/linux/
cp $SPACK_ROOT/bluebrain/sysconfig/jusuf/* $SPACK_ROOT/etc/spack/defaults/linux/

# Directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME
export HOME=/p/home/jusers/blancoalonso1/jusuf
module list

MIRROR_PATH=$DEPLOYMENT_HOME/mirrors
[[ -d $MIRROR_PATH ]] || (spack mirror rm local_filesystem && spack mirror add local_filesystem $MIRROR_PATH)
echo $MIRROR_PATH
spack mirror add local_filesystem $MIRROR_PATH
spack mirror list

# create environment
# DO ONLY ONCE
#spack env create myenv
#spack env activate myenv

# Python 3 packages
module load SciPy-Stack/2023a
module load SciPy-bundle/2023.07
#module unload XZ/.5.2.5
module list
export LC_ALL=en_US.utf8
export LANG=en_US.utf8
export LC_CTYPE=en_US.UTF-8

PYTHON_VERSION='^python@3.11.3'
#neurodamus_deps="^coreneuron $PYTHON_VERSION ^diffutils%gcc"

spack spec -Il neurodamus-hippocampus+coreneuron %intel
#for nd in neurodamus-hippocampus neurodamus-neocortex neurodamus-mousify
#do
#   spack install --keep-stage --dirty -v $nd+coreneuron %intel $neurodamus_deps
#done

spack spec -Il py-neurodamus%intel $PYTHON_VERSION
#spack install --dirty --keep-stage py-neurodamus%intel $PYTHON_VERSION

#spack spec -Il neuron~mpi %intel $PYTHON_VERSION
#spack install --dirty --keep-stage -v neuron~mpi %intel $PYTHON_VERSION

#spack spec -Il py-bluepy%gcc $PYTHON_VERSION
#spack install --dirty --keep-stage -v py-bluepy%gcc $PYTHON_VERSION

#spack spec -Il py-sonata-network-reduction%gcc $PYTHON_VERSION ^libzmq%intel
#spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc $PYTHON_VERSION ^libzmq%intel

#spack uninstall py-bluepyopt
#spack spec -Il py-bluepyopt%gcc $PYTHON_VERSION ^libzmq%intel
#spack install --keep-stage --dirty -v py-bluepyopt%gcc $PYTHON_VERSION ^libzmq%intel

#spack spec -Il psp-validation%gcc $PYTHON_VERSION ^libzmq%intel
#spack install --dirty psp-validation%gcc $PYTHON_VERSION ^libzmq%intel

#spack spec -Il emsim%gcc $PYTHON_VERSION
#spack install --dirty --keep-stage emsim%gcc $PYTHON_VERSION ldlibs="-lpthread"

#spack spec -Il py-netpyne%gcc $PYTHON_VERSION ^coreneuron%intel
#spack install --dirty --keep-stage py-netpyne%gcc $PYTHON_VERSION ^coreneuron%intel

#spack concretize -f
#spack python $DEPLOYMENT_HOME/hashes.py | tee $DEPLOYMENT_HOME/specs.txt
#cat $DEPLOYMENT_HOME/specs.txt

#shas="$(cut -d" " -f1 $DEPLOYMENT_HOME/specs.txt)"

# Re-generate modules
spack module lmod refresh --delete-tree -y #${shas}

#cd $DEPLOYMENT_HOME/modules/tcl/linux-rocky8-zen2
#ind py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'