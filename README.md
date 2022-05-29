# manga-dlp

## python script to download mangas

[![status-badge](https://ci.44net.ch/api/badges/olofvndrhr/manga-dlp/status.svg)](https://ci.44net.ch/olofvndrhr/manga-dlp)
[![Quality Gate Status](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=alert_status&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Coverage](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=coverage&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Bugs](https://sonarqube.44net.ch/api/project_badges/measure?project=olofvndrhr%3Amanga-dlp&metric=bugs&token=f9558470580eea5b4899cf33f190eee16011346d)](https://sonarqube.44net.ch/dashboard?id=olofvndrhr%3Amanga-dlp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

### With pip (pypi)

(not yet done)

### With docker

See the docker [README](./docker/README.md)

## Options

> "--format" currently only works with "", "pdf", "zip", "rar" and "cbz". As it just renames the zip file with the new
> suffix (except pdf). For pdf creation you have to install img2pdf.

```txt
usage: manga-dlp.py [-h] (-u URL_UUID | --read READ | -v) [-c CHAPTERS] [-p PATH] [-l LANG] [--list] [--format FORMAT] [--forcevol] [--wait WAIT] [--verbose]

Script to download mangas from various sites

options:
-h, --help                          show this help message and exit
-u URL_UUID, --url URL_UUID         URL or UUID of the manga
--read READ                         Path of file with manga links to download. One per line
-v, --version                       Show version of manga-dlp and exit
-c CHAPTERS, --chapters CHAPTERS    Chapters to download
-p PATH, --path PATH                Download path. Defaults to "<script_dir>/downloads"
-l LANG, --language LANG            Manga language. Defaults to "en" --> english
--list                              List all available chapters. Defaults to false
--format FORMAT                     Archive format to create. An empty string means dont archive the folder. Defaults to 'cbz'
--forcevol                          Force naming of volumes. For mangas where chapters reset each volume
--wait WAIT                         Time to wait for each picture to download in seconds(float). Defaults 0.5
--verbose                           Verbose logging. Defaults to false
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

## Contribution / Bugs

For suggestions for improvement, just open a pull request.

If you want to add support for a new site, there is an api [template file](./contrib/api_template.py) which you can use.

Otherwise you can open a issue with the name of the site which you want support for. (not guaranteed to be implemented)

If you encounter any bugs, also just open a issue with a description of the problem.

## TODO's

- <del>Make docker container for easy distribution</del>
  --> [Dockerhub](https://hub.docker.com/repository/docker/olofvndrhr/manga-dlp)
- <del>Automate release</del>
  --> Done with woodpecker-ci
- Make pypi package
- Add more supported sites
