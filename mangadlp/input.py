import argparse
import mangadlp.app as app

mangadlp_version = "2.1.0"


def call_app(args):
    # check if --version was used
    if args.version:
        print(f"manga-dlp version: {mangadlp_version}")
        exit(0)
    # call main function with all input arguments
    mdlp = app.MangaDLP(
        args.url_uuid,
        args.lang,
        args.chapters,
        args.read,
        args.list,
        args.format,
        args.forcevol,
        args.path,
        args.wait,
        args.verbose,
    )
    mdlp.__main__()


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

    call_app(args)


if __name__ == "__main__":
    get_args()
