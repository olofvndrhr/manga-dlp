#!/bin/bash

# script to set the version numbers on all files

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

# main function
function main () {
  mdlp_version="${1}"
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

# check options
case "${1}" in
  '--help'|'-h'|'help')
    show_help
  ;;
  *)
    main "${@}"
  ;;
esac

