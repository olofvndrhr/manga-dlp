import argparse
import sys
from pathlib import Path

from mangadlp import app, logger
from mangadlp.__about__ import __version__
from mangadlp.logger import Logger

# prepare logger
log = Logger(__name__)


def check_args(args):
    # set logger formatting
    logger.format_logger(args.verbosity)
    # check if --version was used
    if args.version:
        print(f"manga-dlp version: {__version__}")
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
    log.verbose(f"Reading in list '{str(list_file)}'")
    try:
        url_str = list_file.read_text(encoding="utf-8")
        url_list = url_str.splitlines()
    except Exception as exc:
        raise IOError from exc

    # filter empty lines and remove them
    filtered_list = list(filter(len, url_list))
    log.verbose(f"Mangas from list: {filtered_list}")

    return filtered_list


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
    )
    mdlp.get_manga()


def get_input():
    print(f"manga-dlp version: {__version__}")
    print("Enter details of the manga you want to download:")
    while True:
        try:
            url_uuid = str(input("Url or UUID: "))
            readlist = str(input("List with links (optional): "))
            language = str(input("Language: ")) or "en"
            list_chapters = str(input("List chapters? y/N: "))
            if list_chapters.lower() in {"y", "yes"}:
                chapters = str(input("Chapters: "))
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception:
            continue
        else:
            break

    args = [
        "-l",
        language,
        "-c",
        chapters,
    ]
    if url_uuid:
        args.extend(("-u", url_uuid))
    if readlist:
        args.extend(("--read", readlist))
    if list_chapters.lower() in {"y", "yes"}:
        args.append("--list")

    # start script again with the arguments
    sys.argv.extend(args)
    log.info(f"Args: {sys.argv}")
    get_args()


def get_args():
    parser = argparse.ArgumentParser(
        description="Script to download mangas from various sites"
    )
    action = parser.add_mutually_exclusive_group(required=True)
    verbosity = parser.add_mutually_exclusive_group(required=False)

    action.add_argument(
        "-u",
        "--url",
        "--uuid",
        dest="url_uuid",
        required=False,
        help="URL or UUID of the manga",
        action="store",
    )
    action.add_argument(
        "--read",
        dest="read",
        required=False,
        help="Path of file with manga links to download. One per line",
        action="store",
    )
    action.add_argument(
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
    verbosity.add_argument(
        "--lean",
        dest="verbosity",
        required=False,
        help="Lean logging. Minimal log output. Defaults to false",
        action="store_const",
        const=25,
        default=20,
    )
    verbosity.add_argument(
        "--verbose",
        dest="verbosity",
        required=False,
        help="Verbose logging. More log output. Defaults to false",
        action="store_const",
        const=15,
        default=20,
    )
    verbosity.add_argument(
        "--debug",
        dest="verbosity",
        required=False,
        help="Debug logging. Most log output. Defaults to false",
        action="store_const",
        const=10,
        default=20,
    )

    # parser.print_help()
    args = parser.parse_args()

    check_args(args)


def main():
    if len(sys.argv) > 1:
        get_args()
    else:
        get_input()


if __name__ == "__main__":
    main()
