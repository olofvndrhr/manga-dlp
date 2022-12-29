# manga-dlp - python script to download mangas

> Full docs: https://manga-dlp.ivn.sh

CI/CD

[![status-badge](https://img.shields.io/drone/build/olofvndrhr/manga-dlp?label=tests&server=https%3A%2F%2Fci.44net.ch)](https://ci.44net.ch/olofvndrhr/manga-dlp)
[![Last Release](https://img.shields.io/github/release-date/olofvndrhr/manga-DLP?label=last%20release)](https://github.com/olofvndrhr/manga-dlp/releases)
[![Version](https://img.shields.io/github/v/release/olofvndrhr/manga-dlp?label=git%20release)](https://github.com/olofvndrhr/manga-dlp/releases)
[![Version PyPi](https://img.shields.io/pypi/v/manga-dlp?label=pypi%20release)](https://pypi.org/project/manga-dlp/)

Code Analysis

[![Quality Gate Status](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=alert_status&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Coverage](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=coverage&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Bugs](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=bugs&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Security](https://img.shields.io/snyk/vulnerabilities/github/olofvndrhr/manga-dlp)](https://app.snyk.io/org/olofvndrhr-t6h/project/aae9609d-a4e4-41f8-b1ac-f2561b2ad4e3)

Meta

[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Linter](https://img.shields.io/badge/linter-pylint-yellowgreen)](https://pylint.pycqa.org/en/latest/)
[![Types](https://img.shields.io/badge/types-mypy-blue)](https://github.com/python/mypy)
[![Imports](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort)
[![Tests](https://img.shields.io/badge/tests-pytest%20%7C%20tox-yellow)](https://github.com/pytest-dev/pytest/)
[![Coverage](https://img.shields.io/badge/coverage-coveragepy-green)](https://github.com/nedbat/coveragepy)
[![License](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://snyk.io/learn/what-is-mit-license/)
[![Compatibility](https://img.shields.io/pypi/pyversions/manga-dlp)](https://pypi.org/project/manga-dlp/)
---

## Description

A manga download script written in python. It only supports [mangadex.org](https://mangadex.org/) for now. But support
for other sites is planned.

Before downloading a new chapter, the script always checks if there is already a chapter with the same name in the
download directory. If found the chapter is skipped. So you can run the script on a schedule to only download new
chapters without any additional setup.

The default behaiviour is to pack the images to a [cbz archive](https://en.wikipedia.org/wiki/Comic_book_archive). If
you just want the folder with all the pictures use the flag `--nocbz`.

## _Currently_ Supported sites

- [Mangadex.org](https://mangadex.org/)

## Usage

### Quick start

```sh
python3 manga-dlp.py \
          --url https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu \
          --language "en" \
          --chapters "all"
```

### With GitHub

```sh
git clone https://github.com/olofvndrhr/manga-dlp.git # clone the repository

cd manga-dlp # go in the directory

pip install -r requirements.txt # install required packages

# on windows
python manga-dlp.py <options>
# on unix
python3 manga-dlp.py <options>
```

### With pip ([pypi](https://pypi.org/project/manga-dlp/))

```sh
python3 -m pip install manga-dlp # download the package from pypi

python3 -m mangadlp <args> # start the script as a module
OR
manga-dlp <args> # call script directly
OR
mangadlp <args> # call script directly
```

### With docker

See the docker [README](https://manga-dlp.ivn.sh/docker/)

## Options

```txt
Usage: manga-dlp.py [OPTIONS]

Script to download mangas from various sites

Options:
--help                          Show this message and exit.
--version                       Show the version and exit.

source: [mutually_exclusive, required]
-u, --url, --uuid TEXT          URL or UUID of the manga
--read FILE                     Path of file with manga links to download. One per line

verbosity: [mutually_exclusive]
--loglevel INTEGER              Custom log level  [default: 20]
--warn                          Only log warnings and higher
--debug                         Debug logging. Log EVERYTHING

-c, --chapters TEXT             Chapters to download
-p, --path PATH                 Download path  [default: downloads]
-l, --language TEXT             Manga language  [default: en]
--list                          List all available chapters
--format TEXT                   Archive format to create. An empty string means dont archive the folder  [default: cbz]
--forcevol                      Force naming of volumes. For mangas where chapters reset each volume
--wait FLOAT                    Time to wait for each picture to download in seconds(float)  [default: 0.5]
--hook-manga-pre TEXT           Commands to execute before the manga download starts
--hook-manga-post TEXT          Commands to execute after the manga download finished
--hook-chapter-pre TEXT         Commands to execute before the chapter download starts
--hook-chapter-post TEXT        Commands to execute after the chapter download finished
```

## Contribution / Bugs

For suggestions for improvement, just open a pull request.

If you want to add support for a new site, there is an api [template file](./contrib/api_template.py) which you can use.
And more infos and tools in the contrib [README.md](contrib/README.md)

Otherwise, you can open am issue with the name of the site which you want support for. (not guaranteed to be
implemented)

If you encounter any bugs, also just open an issue with a description of the problem.

## TODO's

- <del>Make docker container for easy distribution</del>
  --> [Dockerhub](https://hub.docker.com/repository/docker/olofvndrhr/manga-dlp)
- <del>Automate release</del>
  --> Done with woodpecker-ci
- <del>Make pypi package</del>
  --> Done with release [2.1.7](https://pypi.org/project/manga-dlp/)
- Add more supported sites
