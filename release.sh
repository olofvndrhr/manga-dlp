#!/bin/bash

# script to set the version numbers on all files

# precheck
if [[ -z "${1}" ]] || [[ -z "${2}" ]]; then
  printf 'Error\n'
  exit 1
fi

# set mdlp version
mdlp_version="${2}"

function show_help(){
  return
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
function set_version () {
  # check for version
  if [[ -z "${mdlp_version}" ]]; then
    printf 'You need to specify a version with $1\n'
    exit 1
  fi
  # set docker versions
  if ! set_ver_docker; then
    printf 'Error\n'; fi
  # set pypi versions
  if ! set_ver_pypi; then
    printf 'Error\n'; fi
}

# create changelog for release
function get_changelog () {
  printf 'Creating changelog\n'
  # check for version
  if [[ -z "${mdlp_version}" ]]; then
    printf 'You need to specify a version with $1\n'
    exit 1
  fi
  awk -v ver="[${mdlp_version}]" \
        '/^## / { if (p) { exit }; if ($2 == ver) { p=1; next } } p && NF' \
          'CHANGELOG.md' > 'RELEASENOTES.md'
  printf 'Done\n'
}

# check options
case "${1}" in
  '--help'|'-h'|'help')
    show_help
  ;;
  '--set-version')
    set_version
  ;;
  '--get-changelog')
    get_changelog
  ;;
  *)
    printf 'Error\n'
    exit 1
  ;;
esac

