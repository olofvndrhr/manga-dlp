#!/bin/bash
# shellcheck disable=SC2016

# script to set the version numbers on all files or generate changelogs for a release

function pre_checks() {
    # prechecks
    if [[ -z "${2}" ]]; then
        printf 'No version was provided\n'
        printf 'Error\n'
        exit 1
    fi
    # set mdlp version
    mdlp_version="${2}"
}

function show_help() {
    printf 'Script to change the version numbers of mangadlp in the build files, or generate release-notes for a release\n'
    printf '\nUsage:\n'
    printf '  ./release.sh <option> <mdlp-version>\n'
    printf '\nOptions:\n'
    printf '  --set-version         - Set version number on all build files\n'
    printf '  --get-changelog       - Create RELEASENOTES.md for github/gitea release\n'
    printf '\nExample:\n'
    printf '  ./release.sh --get-releasenotes "2.0.5"\n'
    exit 1
}

function set_ver_docker() {
    printf 'Changing version in docker-files\n'
    local docker_files docker_regex
    docker_files=(
        'docker/Dockerfile.amd64'
        'docker/Dockerfile.arm64'
    )
    docker_regex='s,^ARG MDLP_VERSION=.*$,ARG MDLP_VERSION='"${mdlp_version}"',g'
    for file in "${docker_files[@]}"; do
        if ! sed -i "${docker_regex}" "${file}"; then return 1; fi
    done
    printf 'Done\n'
}

function set_ver_pypi() {
    printf 'Changing version in pypi-files\n'
    local pypi_files pypi_regex
    pypi_files=(
        'setup.py'
    )
    pypi_regex='s/version=.*$/version=\"'"${mdlp_version}"'\",/g'
    for file in "${pypi_files[@]}"; do
        if ! sed -i "${pypi_regex}" "${file}"; then return 1; fi
    done
    printf 'Done\n'
}

# set version number in files
function set_version() {
    # check for version
    if [[ -z "${mdlp_version}" ]]; then
        printf 'You need to specify a version with $1\n'
        exit 1
    fi
    # set docker versions
    if ! set_ver_docker; then
        printf 'Error\n'
    fi
    # set pypi versions
    if ! set_ver_pypi; then
        printf 'Error\n'
    fi
}

# create changelog for release
function get_releasenotes() {
    printf 'Creating release-notes\n'
    # check for version
    if [[ -z "${mdlp_version}" ]]; then
        printf 'You need to specify a version with $1\n'
        exit 1
    fi
    awk -v ver="[${mdlp_version}]" \
        '/^## / { if (p) { exit }; if ($2 == ver) { p=1; next } } p && NF' \
        'CHANGELOG.md' >'RELEASENOTES.md'
    printf 'Done\n'
}

# check options
case "${1}" in
'--help' | '-h' | 'help')
    show_help
    ;;
'--set-version')
    pre_checks "${@}"
    set_version
    ;;
'--get-releasenotes')
    pre_checks "${@}"
    get_releasenotes
    ;;
*)
    show_help
    ;;
esac
