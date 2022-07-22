#!/bin/bash
# shellcheck disable=SC2016

# script to extract the release notes from the changelog

# show script help
function show_help() {
    cat << EOF

    Script to generate release-notes from a changelog (CHANGELOG.md)
    Usage:
      ./get_release_notes.sh <new_version>


    Example:
      ./get_release_notes.sh "2.0.5"

EOF
    exit 0
}

# create changelog for release
function get_release_notes() {
    local l_version="${1}"

    printf 'Creating release-notes\n'
    # check for version
    if [[ -z "${l_version}" ]]; then
        printf 'You need to specify a version with $1\n'
        exit 1
    fi
    if [[ ${l_version,,} == "latest" ]]; then
        l_version="$(grep -o -E "^##\s\[[0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}\]" CHANGELOG.md | head -n 1 | grep -o -E "[0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}")"
    fi
    awk -v ver="[${l_version}]" \
        '/^## / { if (p) { exit }; if ($2 == ver) { p=1 } } p && NF' \
        'CHANGELOG.md' > 'RELEASENOTES.md'
    printf 'Done\n'
}

# check options
case "${1}" in
    '--help' | '-h' | 'help')
        show_help
        ;;
    *)
        get_release_notes "${@}"
        ;;
esac
