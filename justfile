#!/usr/bin/env just --justfile

default: show_receipts

set shell := ["bash", "-uc"]
set dotenv-load := true
#set export

# aliases
alias s := show_receipts
alias i := show_system_info
alias p := prepare_workspace
alias t := tests
alias f := tests_full

# variables
export asdf_version := "v0.10.2"

# default recipe to display help information
show_receipts:
    @just --list

show_system_info:
    @echo "=================================="
    @echo "os : {{os()}}"
    @echo "arch: {{arch()}}"
    @echo "home: ${HOME}"
    @echo "project dir: {{justfile_directory()}}"
    @echo "=================================="

check_asdf:
    @if ! asdf --version; then \
        just install_asdf \
    ;else \
        echo "asdf already installed" \
    ;fi
    just install_asdf_bins

install_asdf:
    @echo "installing asdf"
    @echo "asdf version: ${asdf_version}"
    @git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch "${asdf_version}"
    @echo "adding asdf to .bashrc"
    @if ! grep -q ".asdf/asdf.sh" "${HOME}/.bashrc"; then \
        echo -e '\n# source asdf' >> "${HOME}/.bashrc" \
        ;echo 'source "${HOME}/.asdf/asdf.sh"' >> "${HOME}/.bashrc" \
        ;echo -e 'source "${HOME}/.asdf/completions/asdf.bash"\n' >> "${HOME}/.bashrc" \
    ;fi
    @echo "to load asdf either restart your shell or do: 'source \${HOME}/.bashrc'"

setup_asdf:
    @echo "installing asdf bins"
    # add plugins
    @if ! asdf plugin add python; then :; fi
    @if ! asdf plugin add shfmt; then :; fi
    @if ! asdf plugin add shellcheck; then :; fi
    @if ! asdf plugin add just https://github.com/franklad/asdf-just; then :; fi
    @if ! asdf plugin add direnv; then :; fi
    # install bins
    @if ! asdf install; then :; fi
    # setup direnv
    @if ! asdf direnv setup --shell bash --version latest; then :; fi

create_venv:
    @echo "creating venv"
    @python3 -m pip install --upgrade pip setuptools wheel
    @python3 -m venv venv

test_shfmt:
    @find . -type f \( -name "**.sh" -and -not -path "./venv/*" -and -not -path "./.tox/*" \) -exec shfmt -d -i 4 -bn -ci -sr "{}" \+;

test_black:
    @python3 -m black --check --diff .

test_isort:
    @python3 -m isort --check-only --diff .

test_mypy:
    @python3 -m mypy --install-types --non-interactive mangadlp/

test_pytest:
    @python3 -m pytest -x

test_tox:
    @python3 -m tox

test_tox_coverage:
    @python3 -m tox -e coverage

test_build:
    @python3 -m hatch build

test_ci_conf:
    @woodpecker-cli lint .woodpecker/

test_docker_build:
    @docker build . -f docker/Dockerfile.amd64 -t manga-dlp:test

# install dependecies and set everything up
prepare_workspace:
     just show_system_info
     just check_asdf
     just setup_asdf
     just create_venv

tests:
    just show_system_info
    -just test_ci_conf
    just test_shfmt
    just test_black
    just test_isort
    just test_mypy
    just test_pytest
    @echo -e "\n\033[0;32m=== ALL DONE ===\033[0m\n"

tests_full:
    just show_system_info
    -just test_ci_conf
    just test_shfmt
    just test_black
    just test_isort
    just test_mypy
    just test_build
    just test_tox
    just test_tox_coverage
    just test_docker_build
    @echo -e "\n\033[0;32m=== ALL DONE ===\033[0m\n"
