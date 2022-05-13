import re
from pathlib import Path

import mangadlp.downloader as downloader
import mangadlp.utils as utils

# supported api's
from mangadlp.api.mangadex import Mangadex


class AppArguments:
    def __init__(self, args: dict):
        self.api = args["api"]
        self.url_uuid = args["url_uuid"]
        self.language = args["language"]
        self.chapters = args["chapters"]
        self.readlist = args["readlist"]
        self.list_chapters = args["list_chapters"]
        self.file_format = args["file_format"]
        self.forcevol = args["forcevol"]
        self.download_path = args["chapter_path"]
        self.download_wait = args["download_wait"]
        self.verbose = args["verbose"]


def main(
    url_uuid: str = "",
    language: str = "en",
    chapters: str = None,
    readlist: str = "",
    list_chapters: bool = False,
    file_format: str = "cbz",
    forcevol: bool = False,
    download_path: str = "downloads",
    download_wait: float = 0.5,
    verbose: bool = False,
) -> None:
    """Download Mangas from supported sites

    :param url_uuid: URL or UUID of the manga
    :param language: Manga language with country codes. "en" --> english
    :param chapters: Chapters to download, "all" for every chapter available
    :param readlist: Path of file with manga links to download. One per line
    :param list_chapters: List all available chapters and exit
    :param file_format: Archive format to create. An empty string means don't archive the folder
    :param forcevol: Force naming of volumes. Useful for mangas where chapters reset each volume
    :param download_path: Download path. Defaults to '<script_dir>/downloads'
    :param download_wait: Time to wait for each picture to download in seconds
    :param verbose: If verbose logging is enabled

    :return: Nothing. Just the files
    """

    # prechecks userinput/options
    if not list_chapters and chapters is None:
        # no chapters to download were given
        print(
            f'ERR: You need to specify one or more chapters to download. To see all chapters use "--list"'
        )
        exit(1)
    # no url and no readin list given
    if not url_uuid and not readlist:
        print(
            f'ERR: You need to specify a manga url/uuid with "-u" or a list with "--read"'
        )
        exit(1)
    # url and readin list given
    if url_uuid and readlist:
        print(f'ERR: You can only use "-u" or "--read". Dont specify both')
        exit(1)

    # create arguments dict for class creation
    mdlp_args = {
        "url_uuid": url_uuid,
        "language": language,
        "chapters": chapters,
        "readlist": readlist,
        "list_chapters": list_chapters,
        "file_format": file_format,
        "forcevol": forcevol,
        "chapter_path": download_path,
        "download_wait": download_wait,
        "verbose": verbose,
    }

    # check if readin file was specified
    if readlist:
        # loop trough every link in readin file
        for url in readin_list(readlist):
            api_used = check_api(url)
            if not api_used:
                print(f"ERR: No API matched for: {url}. Skipping")
                continue
            # add api used to dict
            mdlp_args["api"] = api_used
            # create class
            args = AppArguments(mdlp_args)
            # get manga
            get_manga(args)
    else:
        # single manga
        api_used = check_api(url_uuid)
        if not api_used:
            print(f"ERR: No API matched for: {url_uuid}. Skipping")
            exit(1)
        # add api used to dict
        mdlp_args["api"] = api_used
        # create class
        args = AppArguments(mdlp_args)
        # get manga
        get_manga(args)


# read in the list of links from a file
def readin_list(manga_readlist):
    url_file = Path(manga_readlist)
    url_list = []
    with url_file.open("r") as file:
        for line in file:
            url_list.append(line.rstrip())

    return url_list


# check the api which needs to be used
def check_api(manga_url):
    # apis to check
    api_mangadex = re.compile("mangadex.org")
    api_mangadex2 = re.compile(
        "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
    )
    api_test = re.compile("test.test")

    # check url for match
    if api_mangadex.search(manga_url) or api_mangadex2.search(manga_url):
        return Mangadex

    # this is only for testing multiple apis
    if api_test.search(manga_url):
        print("Not supported yet")
        exit(1)

    # no supported api found
    print(f"ERR: No supported api in link/uuid found: {manga_url}")
    return False


# main function to get the chapters
def get_manga(args: AppArguments) -> None:
    # show api used
    if args.verbose:
        print(f"INFO: API used: {args.api}")
    # init api
    api = args.api(args.url_uuid, args.language, args.forcevol, args.verbose)
    # get manga title and uuid
    manga_uuid = api.manga_uuid
    manga_title = api.manga_title
    # crate chapter list
    manga_chapter_list = api.create_chapter_list()
    # create skipped chapters list
    skipped_chapters = []

    # show infos
    print_divider = "========================================="
    print(f"\n{print_divider}")
    print(f"INFO: Manga Name: {manga_title}")
    print(f"INFO: Manga UUID: {manga_uuid}")
    print(f"INFO: Total chapters: {len(manga_chapter_list)}")

    # list chapters if list_chapters is true
    if args.list_chapters:
        print(f"INFO: Available Chapters:\n{', '.join(manga_chapter_list)}")
        print(f"{print_divider}\n")
        return

    # check chapters to download if not all
    if args.chapters.lower() == "all":
        chapters_to_download = manga_chapter_list
    else:
        chapters_to_download = utils.get_chapter_list(args.chapters)

    # show chapters to download
    print(f"INFO: Chapters selected:\n{', '.join(chapters_to_download)}")
    print(f"{print_divider}\n")

    # create manga folder
    manga_path = Path(f"{args.download_path}/{manga_title}")
    manga_path.mkdir(parents=True, exist_ok=True)

    # main download loop
    for chapter in chapters_to_download:
        # get chapter infos
        chapter_infos = api.get_chapter_infos(chapter)

        # get image urls for chapter
        try:
            chapter_image_urls = api.get_chapter_images(chapter, args.download_wait)
        except KeyboardInterrupt:
            print("ERR: Stopping")
            exit(1)

        # check if the image urls are empty. if yes skip this chapter (for mass downloads)
        if not chapter_image_urls:
            print(
                f"ERR: Skipping Vol. {chapter_infos['volume']} Ch.{chapter_infos['chapter']}"
            )
            # add to skipped chapters list
            skipped_chapters.append(
                f"{chapter_infos['volume']}:{chapter_infos['chapter']}"
            ) if args.forcevol else skipped_chapters.append(chapter_infos["chapter"])

            continue

        # get filename for chapter
        chapter_filename = api.get_filename(chapter)

        # set download path for chapter
        chapter_path = manga_path / chapter_filename

        # check if chapter already exists.
        # check for folder if option nocbz is given. if nocbz is not given, the folder will be overwritten

        if utils.check_existence(chapter_path, args.file_format):
            print(
                f"INFO: '{chapter_filename}.{args.file_format}' already exists. Skipping\n"
                if args.file_format
                else f"'{chapter_filename}' already exists. Skipping\n"
            )
            continue

        # create chapter folder (skips it if it already exists)
        chapter_path.mkdir(parents=True, exist_ok=True)

        # verbose log
        if args.verbose:
            print(f"INFO: Chapter UUID: {chapter_infos['uuid']}")
            print(
                f"INFO: Filename: '{chapter_filename}.{args.file_format}'\n"
                if args.file_format
                else f"INFO: Filename: '{chapter_filename}'\n"
            )
            print(f"INFO: Image URLS:\n{chapter_image_urls}\n")

        # log
        print(f"INFO: Downloading: '{chapter_filename}'")

        # download images
        try:
            downloader.download_chapter(
                chapter_image_urls, chapter_path, args.download_wait, args.verbose
            )
        except KeyboardInterrupt:
            print("ERR: Stopping")
            exit(1)
        except:
            print(f"ERR: Cant download: '{chapter_filename}'. Exiting")

        else:
            # Done with chapter
            print(f"INFO: Successfully downloaded: '{chapter_filename}'")

        # create archive for chapter
        if args.file_format:
            print(f"INFO: Creating '{args.file_format}' archive")
            try:
                utils.make_archive(chapter_path, args.file_format)
            except:
                print("ERR: Could not create '{file_format}' archive")
                exit(1)

        # done with chapter
        print("INFO: Done with chapter")
        print("-----------------------------------------\n")

    # done with manga
    print(f"{print_divider}")
    print(f"INFO: Done with manga: {manga_title}")
    if len(skipped_chapters) >= 1:
        print(f"INFO: Skipped chapters:\n{', '.join(skipped_chapters)}")
    print(f"{print_divider}\n")
