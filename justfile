#!/usr/bin/env just --justfile

default: show_receipts

set shell := ["bash", "-uc"]
set dotenv-load := true

show_receipts:
    just --list

show_system_info:
    @echo "=================================="
    @echo "os : {{ os() }}"
    @echo "arch: {{ arch() }}"
    @echo "justfile dir: {{ justfile_directory() }}"
    @echo "invocation dir: {{ invocation_directory() }}"
    @echo "running dir: `pwd -P`"
    @echo "=================================="

setup:
    asdf install
    lefthook install

create_venv:
    @echo "creating venv"
    pip install --upgrade pip setuptools wheel
    python3 -m venv venv

install_deps:
    @echo "installing dependencies"
    hatch dep show requirements --project-only > /tmp/requirements.txt
    pip install -r /tmp/requirements.txt

install_deps_dev:
    @echo "installing dev dependencies"
    hatch dep show requirements --project-only > /tmp/requirements.txt
    hatch dep show requirements --env-only >> /tmp/requirements.txt
    pip install -r /tmp/requirements.txt

create_reqs:
    @echo "creating requirements"
    hatch dep show requirements --project-only > requirements.txt

test_shfmt:
    find . -type f \( -name "**.sh" -and -not -path "./.**" -and -not -path "./venv**" \) -exec shfmt -d -i 4 -bn -ci -sr "{}" \+;

format_shfmt:
    find . -type f \( -name "**.sh" -and -not -path "./.**" -and -not -path "./venv**" \) -exec shfmt -w -i 4 -bn -ci -sr "{}" \+;

lint:
    just show_system_info
    just test_shfmt
    hatch run lint:style
    hatch run lint:typing

format:
    just show_system_info
    just format_shfmt
    hatch run lint:fmt

check:
    just format
    just lint

test *args:
    hatch run test:test {{ args }}

coverage:
    hatch run test:cov

build:
    hatch build --clean

run loglevel *flags:
    hatch run mangadlp --loglevel {{ loglevel }} {{ flags }}
