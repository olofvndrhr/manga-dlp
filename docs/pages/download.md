# Download mangas

## File-structure

```txt
.
└── <download path>/
    └── <manga title>/
        └── <chapter title>/
```

**Example:**

```txt
./downloads/mangatitle/chaptertitle(.cbz)
```

## Select chapters to download

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

## Set download path

With the option `-p/--path` you can specify a path to download the chapters to. The default path
is `<script_dir>/downloads`. Absolute and relative paths are supported.

**Example:**

`python3 manga-dlp.py <other options> --path /media/mangas`

This will save all mangas/chapters in the path `/media/mangas/<manga title>/<chapter name>`

## Set output format

> `--format` currently only works with `""`, `"pdf"`, `"zip"`, `"rar"` and `"cbz"`.
> As it just renames the zip file with the new
> suffix (except pdf).

You can specify the output format of the manga images with the `--format` option.
The default is set to `.cbz`, so if no format is given it falls back to `<manga-name>/<chapter_name>.cbz`

For pdf creation you have to install [img2pdf](https://pypi.org/project/img2pdf/).
With the amd64 docker image it is already installed
see more in the Docker [README.md](../docker/).

**Supported format options:**

* cbz - `--format "cbz"` or `--format ".cbz"` **- default**
* cbr - `--format "cbr"` or `--format ".cbr"`
* zip - `--format "zip"` or `--format ".zip"`
* pdf - `--format "pdf"` or `--format ".pdf"`
* _none_ - `--format ""` - this saves the images just in a folder

**Example:**

`python3 manga-dlp.py <other options> --format "zip"`

This will download the chapter and save it as a zip archive.

## Read links from a file

With the option `--read` you can specify a file with links to multiple mangas. They will be parsed from top to bottom
one at a time. Every link will be matched for the right api to use. It is important that you only have one link per
line, otherwise they can't be parsed.

**Example:**

```txt
# mangas.txt
link1
link2
link3
```

`python3 manga-dlp.py --read mangas.txt --list`

This will list all available chapters for link1, link2 and link3.
