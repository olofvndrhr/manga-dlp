import re
from pathlib import Path

import mangadlp.downloader as downloader
import mangadlp.utils as utils

# supported api's
from mangadlp.api.mangadex import Mangadex


def main(
    manga_url_uuid="",
    manga_language="en",
    manga_chapters=None,
    manga_readlist="",
    manga_list_chapters=False,
    manga_nocbz=False,
    manga_forcevol=False,
    download_path="downloads",
    download_wait=0.5,
    log_verbose=False,
):
    """Download Mangas from supported sites\n

    Args:\n
      url (str) -- Manga URL or UUID to Download. No defaults\n
      lang (str) -- Language to download chapters in. Defaults to "en" -> english\n
      chapter (str) -- Chapters to download "all" for every chapter available. Defaults to none\n
      readlist (str) -- List of chapters to read in. One link per line. No defaults\n
      list_chapters (bool) -- If it should only list all available chapters. Defaults to False\n
      nocbz (bool) -- If the downloaded images should not be packed into a .cbz archive. Defaults to false\n
      forcevol (bool) -- Force naming of volumes. For mangas where chapters reset each volume. Defaults to false.\n
      download_path (str) -- Folder to save mangas to. Defaults to "<script_dir>/downloads"\n
      download_wait (float) -- Time to wait for each picture to download in seconds(float). Defaults 0.5.\n
      log_verbose (bool) -- If verbose logging is enabled. Defaults to false\n

    Returns:\n
      nothing\n
    """
    # prechecks userinput/options
    if not manga_list_chapters and manga_chapters is None:
        # no chapters to download were given
        print(
            f'ERR: You need to specify one or more chapters to download. To see all chapters use "--list"'
        )
        exit(1)
    # no url and no readin list given
    elif not manga_url_uuid and not manga_readlist:
        print(
            f'ERR: You need to specify a manga url/uuid with "-u" or a list with "--read"'
        )
        exit(1)
    # url and readin list given
    elif manga_url_uuid and manga_readlist:
        print(f'ERR: You can only use "-u" or "--read". Dont specify both')
        exit(1)

    # check if readin file was specified
    if manga_readlist:
        # loop trough every chapter in readin file
        for url in readin_list(manga_readlist):
            api_used = check_api(url)
            if not api_used:
                continue
            # get manga
            get_manga(
                api_used,
                url,
                manga_language,
                manga_chapters,
                manga_list_chapters,
                manga_nocbz,
                manga_forcevol,
                download_path,
                download_wait,
                log_verbose,
            )
    else:
        # single manga
        api_used = check_api(manga_url_uuid)
        if not api_used:
            exit(1)
        # get manga
        get_manga(
            api_used,
            manga_url_uuid,
            manga_language,
            manga_chapters,
            manga_list_chapters,
            manga_nocbz,
            manga_forcevol,
            download_path,
            download_wait,
            log_verbose,
        )


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
    elif api_test.search(manga_url):
        pass
    # no supported api found
    else:
        print(f"ERR: No supported api in link/uuid found\n{manga_url}")
        return False


# main function to get the chapters
def get_manga(
    api_used,
    manga_url,
    manga_language,
    manga_chapters,
    manga_list_chapters,
    manga_nocbz,
    manga_forcevol,
    download_path,
    download_wait,
    log_verbose,
):
    # show api used
    if log_verbose:
        print(f"INFO: API used: {api_used}")
    # init api
    Api = api_used(manga_url, manga_language, manga_forcevol, log_verbose)
    # get manga title and uuid
    manga_uuid = Api.manga_uuid
    manga_title = Api.manga_title
    # crate chapter list
    manga_chapter_list = Api.create_chapter_list()

    # show infos
    print_divider = "========================================="
    print(f"\n{print_divider}")
    print(f"INFO: Manga Name: {manga_title}")
    print(f"INFO: Manga UUID: {manga_uuid}")
    print(f"INFO: Total chapters: {len(manga_chapter_list)}")

    # list chapters if manga_list_chapters is true
    if manga_list_chapters:
        print(f'INFO: Available Chapters:\n{", ".join(manga_chapter_list)}')
        print(f"{print_divider}\n")
        return

    # check chapters to download if not all
    if manga_chapters.lower() == "all":
        chapters_to_download = manga_chapter_list
    else:
        chapters_to_download = utils.get_chapter_list(manga_chapters)

    # show chapters to download
    print(f'INFO: Chapters selected:\n{", ".join(chapters_to_download)}')
    print(f"{print_divider}\n")

    # create manga folder
    manga_path = Path(f"{download_path}/{manga_title}")
    manga_path.mkdir(parents=True, exist_ok=True)

    # main download loop
    for chapter in chapters_to_download:
        # get chapter infos
        chapter_infos = Api.get_chapter_infos(chapter)

        # get image urls for chapter
        chapter_image_urls = Api.get_chapter_images(chapter, download_wait)

        # get filename for chapter
        chapter_filename = Api.get_filename(chapter)

        # set download path for chapter
        chapter_path = manga_path / chapter_filename

        # check if chapter already exists.
        # check for folder if option nocbz is given. if nocbz is not given, the folder will be overwritten

        if utils.check_existence(chapter_path, manga_nocbz):
            print(f"INFO: '{chapter_filename}' already exists. Skipping\n")
            continue

        # create chapter folder (skips it if it already exists)
        chapter_path.mkdir(parents=True, exist_ok=True)

        # verbose log
        if log_verbose:
            print(f"INFO: Chapter UUID: {chapter_infos['uuid']}")
            print(
                f"INFO: Filename: '{chapter_filename}'\n"
                if manga_nocbz
                else f"INFO: Filename: '{chapter_filename}.cbz'\n"
            )
            print(f"INFO: Image URLS: {chapter_image_urls}")

        # log
        print(f"INFO: Downloading: '{chapter_filename}'")

        # download images
        try:
            downloader.download_chapter(
                chapter_image_urls, chapter_path, download_wait, log_verbose
            )
        except KeyboardInterrupt:
            print("ERR: Stopping")
            exit(1)
        except:
            print(f"ERR: Cant download: '{chapter_filename}'. Exiting")

        else:
            # Done with chapter
            print(f"INFO: Successfully downloaded: '{chapter_filename}'")

        # make cbz of folder
        if not manga_nocbz:
            print("INFO: Creating .cbz archive")
            try:
                utils.make_archive(chapter_path)
            except:
                print("ERR: Could not make cbz archive")
                exit(1)

        # done with chapter
        print("INFO: Done with chapter")
        print("-----------------------------------------\n")

    # done with manga
    print(f"{print_divider}")
    print(f"INFO: Done with manga: {manga_title}")
    print(f"{print_divider}\n")
