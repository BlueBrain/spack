#!/bin/bash -l

# This script assumes that the following variables are set in the environment:
#
# DEPLOYMENT_ROOT: path to deploy to

set -o errexit
set -o nounset

DEFAULT_DEPLOYMENT_ROOT="/gpfs/bbp.cscs.ch/apps/hpc/test/$(whoami)/deployment"
DEFAULT_DEPLOYMENT_DATA="/gpfs/bbp.cscs.ch/data/project/proj20/pramod_scratch/SPACK_DEPLOYMENT/download"
DEFAULT_DEPLOYMENT_DATE="$(date +%Y-%m-%d)"

# Set variables to default. The user may override the following:
#
# * `DEPLOYMENT_ROOT` for the installation directory
# * `DEPLOYMENT_DATA` containing tarballs of proprietary software
# * `DEPLOYMENT_DATE` to force a date for the installation directory
#
# for the latter, see also the comment of `last_install_dir`
DEPLOYMENT_DATA=${DEPLOYMENT_DATA:-${DEFAULT_DEPLOYMENT_DATA}}
DEPLOYMENT_ROOT=${DEPLOYMENT_ROOT:-${DEFAULT_DEPLOYMENT_ROOT}}
SPACK_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror"
export DEPLOYMENT_ROOT SPACK_MIRROR_DIR

. ./deploy.lib

usage() {
    echo "usage: $0 [-gi] stage...1>&2"
    exit 1
}

do_archive=default
do_generate=default
do_install=default
while getopts "agi" arg; do
    case "${arg}" in
        a)
            do_archive=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_generate} = "default" ]] && do_generate=no
            ;;
        g)
            do_generate=yes
            [[ ${do_install} = "default" ]] && do_install=no
            ;;
        i)
            do_install=yes
            [[ ${do_generate} = "default" ]] && do_generate=no
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND - 1))

if [[ "$@" = "all" ]]; then
    set -- ${stages}
else
    unknown=
    for what in "$@"; do
        if [[ ! ${spec_definitions[${what}]+_} ]]; then
            unknown="${unknown} ${what}"
        fi
    done
    if [[ -n "${unknown}" ]]; then
        echo "unknown stage(s):${unknown}"
        echo "allowed:          ${stages}"
        exit 1
    fi
fi

declare -A desired
for what in "$@"; do
    desired[${what}]=Yes
done

unset $(set +x; env | awk -F= '/^(PMI|SLURM)_/ {print $1}' | xargs)

if [[ "${do_archive}" = "yes" ]]; then
    echo BAS
fi

[[ ${do_generate} != "no" ]] && generate_specs "$@"
for what in ${stages}; do
    if [[ ${desired[${what}]+_} && ${do_install} != "no" ]]; then
        install_specs ${what}
    fi
done
