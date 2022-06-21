import argparse
import sys
from pathlib import Path

import mangadlp.app as app

MDLP_VERSION = "2.1.6"


def check_args(args):
    # check if --version was used
    if args.version:
        print(f"manga-dlp version: {MDLP_VERSION}")
        sys.exit(0)
    # check if a readin list was provided
    if not args.read:
        # single manga, no readin list
        call_app(args)
    else:
        # multiple mangas
        url_list = readin_list(args.read)
        for url in url_list:
            args.url_uuid = url
            call_app(args)


# read in the list of links from a file
def readin_list(readlist: str) -> list:
    list_file = Path(readlist)
    try:
        url_str = list_file.read_text()
        url_list = url_str.splitlines()
    except:
        raise IOError

    return url_list


def call_app(args):
    # call main function with all input arguments
    mdlp = app.MangaDLP(
        args.url_uuid,
        args.lang,
        args.chapters,
        args.list,
        args.format,
        args.forcevol,
        args.path,
        args.wait,
        args.verbose,
    )
    mdlp.get_manga()


def get_args():
    parser = argparse.ArgumentParser(
        description="Script to download mangas from various sites"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-u",
        "--url",
        "--uuid",
        dest="url_uuid",
        required=False,
        help="URL or UUID of the manga",
        action="store",
    )
    group.add_argument(
        "--read",
        dest="read",
        required=False,
        help="Path of file with manga links to download. One per line",
        action="store",
    )
    group.add_argument(
        "-v",
        "--version",
        dest="version",
        required=False,
        help="Show version of manga-dlp and exit",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--chapters",
        dest="chapters",
        required=False,
        help="Chapters to download",
        action="store",
    )
    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        required=False,
        help='Download path. Defaults to "<script_dir>/downloads"',
        action="store",
        default="downloads",
    )
    parser.add_argument(
        "-l",
        "--language",
        dest="lang",
        required=False,
        help='Manga language. Defaults to "en" --> english',
        action="store",
        default="en",
    )
    parser.add_argument(
        "--list",
        dest="list",
        required=False,
        help="List all available chapters. Defaults to false",
        action="store_true",
    )
    parser.add_argument(
        "--format",
        dest="format",
        required=False,
        help="Archive format to create. An empty string means dont archive the folder. Defaults to 'cbz'",
        action="store",
        default="cbz",
    )
    parser.add_argument(
        "--forcevol",
        dest="forcevol",
        required=False,
        help="Force naming of volumes. For mangas where chapters reset each volume",
        action="store_true",
    )
    parser.add_argument(
        "--wait",
        dest="wait",
        required=False,
        type=float,
        default=0.5,
        help="Time to wait for each picture to download in seconds(float). Defaults 0.5",
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        required=False,
        help="Verbose logging. Defaults to false",
        action="store_true",
    )

    # parser.print_help()
    args = parser.parse_args()

    check_args(args)


if __name__ == "__main__":
    get_args()
