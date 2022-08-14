# manga-dlp

## python script to download mangas

#### CI/CD:

[![status-badge](https://img.shields.io/drone/build/olofvndrhr/manga-dlp?label=tests&server=https%3A%2F%2Fci.44net.ch)](https://ci.44net.ch/olofvndrhr/manga-dlp)
[![Last Release](https://img.shields.io/github/release-date/olofvndrhr/manga-DLP?label=last%20release)](https://github.com/olofvndrhr/manga-dlp/releases)
[![Version](https://img.shields.io/github/v/release/olofvndrhr/manga-dlp?label=git%20release)](https://github.com/olofvndrhr/manga-dlp/releases)
[![Version PyPi](https://img.shields.io/pypi/v/manga-dlp?label=pypi%20release)](https://pypi.org/project/manga-dlp/)

#### Code Analysis:

[![Quality Gate Status](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=alert_status&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Coverage](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=coverage&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Bugs](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=bugs&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Security](https://img.shields.io/snyk/vulnerabilities/github/olofvndrhr/manga-dlp)](https://app.snyk.io/org/olofvndrhr-t6h/project/aae9609d-a4e4-41f8-b1ac-f2561b2ad4e3)

#### Meta:

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

See the docker [README](./docker/README.md)

## Options

```txt
usage: manga-dlp.py [-h] (-u URL_UUID | --read READ | -v) [-c CHAPTERS] [-p PATH] [-l LANG] [--list] [--format FORMAT] [--forcevol] [--wait WAIT] [--lean | --verbose | --debug] [--hook-manga-pre HOOK_MANGA_PRE]
[--hook-manga-post HOOK_MANGA_POST] [--hook-chapter-pre HOOK_CHAPTER_PRE] [--hook-chapter-post HOOK_CHAPTER_POST]

Script to download mangas from various sites

optional arguments:
-h, --help                                      show this help message and exit
-u URL_UUID, --url URL_UUID, --uuid URL_UUID    URL or UUID of the manga
--read READ                                     Path of file with manga links to download. One per line
-v, --version                                   Show version of manga-dlp and exit
-c CHAPTERS, --chapters CHAPTERS                Chapters to download
-p PATH, --path PATH                            Download path. Defaults to "<script_dir>/downloads"
-l LANG, --language LANG                        Manga language. Defaults to "en" --> english
--list                                          List all available chapters. Defaults to false
--format FORMAT                                 Archive format to create. An empty string means dont archive the folder. Defaults to 'cbz'
--forcevol                                      Force naming of volumes. For mangas where chapters reset each volume
--wait WAIT                                     Time to wait for each picture to download in seconds(float). Defaults 0.5
--lean                                          Lean logging. Minimal log output. Defaults to false
--verbose                                       Verbose logging. More log output. Defaults to false
--debug                                         Debug logging. Most log output. Defaults to false
--hook-manga-pre HOOK_MANGA_PRE                 Commands to execute before the manga download starts
--hook-manga-post HOOK_MANGA_POST               Commands to execute after the manga download finished
--hook-chapter-pre HOOK_CHAPTER_PRE             Commands to execute before the chapter download starts
--hook-chapter-post HOOK_CHAPTER_POST           Commands to execute after the chapter download finished
```

### Downloads file-structure

```txt
.
└── <download path>/
    └── <manga title>/
        └── <chapter title>/
```

#### Example:

```txt
./downloads/mangatitle/chaptertitle(.cbz)
```

### Select chapters to download

> With the option `-c "all"` you download every chapter available in the selected language

To download specific chapters you can use the option `-c` or `--chapters`. That you don't have to specify all chapters
individually, the script has some logic to fill in the blanks.

Examples:

```sh
# if you want to download chapters 1 to 5
python3 manga-dlp -u <url> -c 1-5

# if you want to download chapters 1 and 5
python3 manga-dlp -u <url> -c 1,5
```

If you use `--forcevol` it's the same, just with the volume number

```sh
# if you want to download chapters 1:1 to 1:5
python3 manga-dlp -u <url> -c 1:1-1:5

# if you want to download chapters 1:1 and 1:5
python3 manga-dlp -u <url> -c 1:1,1:5

# to download the whole volume 1
python3 manga-dlp -u <url> -c 1:
```

And a combination of all

```sh
# if you want to download chapters 1 to 5 and 9
python3 manga-dlp -u <url> -c 1-5,9

# with --forcevol
# if you want to download chapters 1:1 to 1:5 and 9, also the whole volume 4
python3 manga-dlp -u <url> -c 1:1-1:5,1:9,4:
```

### Read list of links from file

With the option `--read` you can specify a file with links to multiple mangas. They will be parsed from top to bottom
one at a time. Every link will be matched for the right api to use. It is important that you only have one link per
line, otherwise they can't be parsed.

#### Example:

```txt
# mangas.txt
link1
link2
link3
```

`python3 manga-dlp.py --read mangas.txt --list`

This will list all available chapters for link1, link2 and link3.

### Set download path

With the option `-p/--path` you can specify a path to download the chapters to. The default path
is `<script_dir>/downloads`. Absolute and relative paths are supported.

#### Example:

`python3 manga-dlp.py <other options> --path /media/mangas`

This will save all mangas/chapters in the path `/media/mangas/<manga title>/<chapter name>`

### Set output format

> `--format` currently only works with `""`, `"pdf"`, `"zip"`, `"rar"` and `"cbz"`.
> As it just renames the zip file with the new
> suffix (except pdf).

You can specify the output format of the manga images with the `--format` option.
The default is set to `.cbz`, so if no format is given it falls back to `<manga-name>/<chapter_name>.cbz`

For pdf creation you have to install [img2pdf](https://pypi.org/project/img2pdf/).
With the amd64 docker image it is already installed
see more in the Docker [README.md](docker/README.md).

#### Supported format options are:

* cbz - `--format "cbz"` or `--format ".cbz"` **- default**
* cbr - `--format "cbr"` or `--format ".cbr"`
* zip - `--format "zip"` or `--format ".zip"`
* pdf - `--format "pdf"` or `--format ".pdf"`
* _none_ - `--format ""` - this saves the images just in a folder

#### Example:

`python3 manga-dlp.py <other options> --format "zip"`

This will download the chapter and save it as a zip archive.

### Hooks

You can run custom hooks with manga-dlp for specific events.
They are run with the `subproccess.call` function, so they get run directly by your operating system.

The available hook events are:

- **Pre Manga** -> Before anything gets downloaded
- **Pre Chapter** -> Before the chapter gets downloaded
- **Post Manga** -> After the manga is done. (All specified chapters were downloaded)
- **Post Chapter** -> After each chapter was downloaded (and formatted if specified)

Each of these hooks can be set with a specific flag:

- `--hook-pre-manga` -> Pre Manga hook
- `--hook-pre-chapter` -> Pre Chapter hook
- `--hook-post-manga` -> Post Manga hook
- `--hook-post-chapter` -> Post Chapter hook

#### Example:

`manga-dlp -u <some url> -c 1 --hook-post-manga <some command>`

`manga-dlp -u <some url> -c 1 --hook-post-manga "echo abc"`

#### Env Variables

All hooks are exposed to a variety of environment variables with infos about the manga/chapter currently downloading.
All available env variables are:

**General:**

- `HOOK_TYPE`
- `STATUS`
- `REASON`

**Manga hooks:**

- `API`
- `MANGA_URL_UUID`
- `MANGA_UUID`
- `MANGA_TITLE`
- `LANGUAGE`
- `TOTAL_CHAPTERS`
- `CHAPTERS_TO_DOWNLOAD`
- `FILE_FORMAT`
- `FORCEVOL`
- `DOWNLOAD_PATH`
- `MANGA_PATH`

**Chapter hooks (extends Manga hooks env variables):**

- `CHAPTER_FILENAME`
- `CHAPTER_PATH`
- `CHAPTER_ARCHIVE_PATH`
- `CHAPTER_UUID`
- `CHAPTER_VOLUME`
- `CHAPTER_NUMBER`
- `CHAPTER_NAME`

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
