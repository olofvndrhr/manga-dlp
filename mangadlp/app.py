import logging
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import mangadlp.downloader as downloader
import mangadlp.utils as utils

# supported api's
from mangadlp.api.mangadex import Mangadex

# prepare logger
log = logging.getLogger(__name__)


class MangaDLP:
    """Download Mangas from supported sites.
    After initialization, start the script with the function get_manga().

    :param url_uuid: URL or UUID of the manga
    :param language: Manga language with country codes. "en" --> english
    :param chapters: Chapters to download, "all" for every chapter available
    :param list_chapters: List all available chapters and exit
    :param file_format: Archive format to create. An empty string means don't archive the folder
    :param forcevol: Force naming of volumes. Useful for mangas where chapters reset each volume
    :param download_path: Download path. Defaults to '<script_dir>/downloads'
    :param download_wait: Time to wait for each picture to download in seconds
    :param verbosity: Verbosity of the output. Uses the logging library values

    :return: Nothing. Just the files
    """

    def __init__(
        self,
        url_uuid: str,
        language: str = "en",
        chapters: str = "",
        list_chapters: bool = False,
        file_format: str = "cbz",
        forcevol: bool = False,
        download_path: str = "downloads",
        download_wait: float = 0.5,
        verbosity: int = 20,
    ) -> None:
        # init parameters
        self.url_uuid = url_uuid
        self.language = language
        self.chapters = chapters
        self.list_chapters = list_chapters
        self.file_format = file_format
        self.forcevol = forcevol
        self.download_path = download_path
        self.download_wait = download_wait
        self.verbosity = verbosity
        # prepare everything
        self._prepare()

    def _prepare(self) -> None:
        # set manga format suffix
        if self.file_format and "." not in self.file_format:
            self.file_format = f".{self.file_format}"
        # start prechecks
        self.pre_checks()
        # init api
        self.api_used = self.check_api(self.url_uuid)
        self.api = self.api_used(self.url_uuid, self.language, self.forcevol)
        # get manga title and uuid
        self.manga_uuid = self.api.manga_uuid
        self.manga_title = self.api.manga_title
        # get chapter list
        self.manga_chapter_list = self.api.chapter_list
        self.manga_path = Path(f"{self.download_path}/{self.manga_title}")

    def pre_checks(self) -> None:
        # prechecks userinput/options
        # no url and no readin list given
        if not self.url_uuid:
            log.error(
                'You need to specify a manga url/uuid with "-u" or a list with "--read"'
            )
            sys.exit(1)
        # checks if --list is not used
        if not self.list_chapters:
            if not self.chapters:
                # no chapters to download were given
                log.error(
                    'You need to specify one or more chapters to download. To see all chapters use "--list"'
                )
                sys.exit(1)
            # if forcevol is used, but didn't specify a volume in the chapters selected
            if self.forcevol and ":" not in self.chapters:
                log.error("You need to specify the volume if you use --forcevol")
                sys.exit(1)
            # if forcevol is not used, but a volume is specified
            if not self.forcevol and ":" in self.chapters:
                log.error("Don't specify the volume without --forcevol")
                sys.exit(1)

    # check the api which needs to be used
    def check_api(self, url_uuid: str) -> type:
        # apis to check
        api_mangadex = re.compile("mangadex.org")
        api_mangadex2 = re.compile(
            "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
        )
        api_test = re.compile("test.test")

        # check url for match
        if api_mangadex.search(url_uuid) or api_mangadex2.search(url_uuid):
            return Mangadex

        # this is only for testing multiple apis
        if api_test.search(url_uuid):
            log.critical("Not supported yet")
            sys.exit(1)

        # no supported api found
        log.error(f"No supported api in link/uuid found: {url_uuid}")
        raise ValueError

    # once called per manga
    def get_manga(self) -> None:
        # create empty skipped chapters list
        skipped_chapters: list[Any] = []
        error_chapters: list[Any] = []

        print_divider = "========================================="
        # show infos
        log.info(f"{print_divider}")
        log.warning(f"Manga Name: {self.manga_title}")
        log.info(f"Manga UUID: {self.manga_uuid}")
        log.info(f"Total chapters: {len(self.manga_chapter_list)}")

        # list chapters if list_chapters is true
        if self.list_chapters:
            log.info(f"Available Chapters: {', '.join(self.manga_chapter_list)}")
            log.info(f"{print_divider}\n")
            return None

        # check chapters to download if not all
        if self.chapters.lower() == "all":
            chapters_to_download = self.manga_chapter_list
        else:
            chapters_to_download = utils.get_chapter_list(
                self.chapters, self.manga_chapter_list
            )

        # show chapters to download
        log.warning(f"Chapters selected: {', '.join(chapters_to_download)}")
        log.info(f"{print_divider}")

        # create manga folder
        self.manga_path.mkdir(parents=True, exist_ok=True)

        # get chapters
        for chapter in chapters_to_download:
            return_infos = self.get_chapter(chapter)
            error_chapters.append(return_infos.get("error"))
            skipped_chapters.append(return_infos.get("skipped"))
            if self.file_format and return_infos["chapter_path"]:
                return_infos = self.archive_chapter(return_infos["chapter_path"])
                error_chapters.append(return_infos.get("error"))
                skipped_chapters.append(return_infos.get("skipped"))
            # check if chapter was skipped
            try:
                return_infos["skipped"]
            # chapter was not skipped
            except KeyError:
                # done with chapter
                log.info(f"Done with chapter '{chapter}'\n")

        # done with manga
        log.info(f"{print_divider}")
        log.warning(f"Done with manga: {self.manga_title}")
        # filter skipped list
        skipped_chapters = list(filter(None, skipped_chapters))
        if len(skipped_chapters) >= 1:
            log.warning(f"Skipped chapters: {', '.join(skipped_chapters)}")
        # filter error list
        error_chapters = list(filter(None, error_chapters))
        if len(error_chapters) >= 1:
            log.warning(f"Chapters with errors: {', '.join(error_chapters)}")

        log.info(f"{print_divider}\n")

    # once called per chapter
    def get_chapter(self, chapter: str) -> dict:
        # get chapter infos
        chapter_infos = self.api.get_chapter_infos(chapter)

        # get image urls for chapter
        try:
            chapter_image_urls = self.api.get_chapter_images(
                chapter, self.download_wait
            )
        except KeyboardInterrupt:
            log.critical("Stopping")
            sys.exit(1)

        # check if the image urls are empty. if yes skip this chapter (for mass downloads)
        if not chapter_image_urls:
            log.error(
                f"No images: Skipping Vol. {chapter_infos['volume']} Ch.{chapter_infos['chapter']}"
            )
            # add to skipped chapters list
            return (
                {
                    "error": f"{chapter_infos['volume']}:{chapter_infos['chapter']}",
                    "chapter_path": None,
                }
                if self.forcevol
                else {"error": f"{chapter_infos['chapter']}", "chapter_path": None}
            )

        # get filename for chapter (without suffix)
        chapter_filename = utils.get_filename(
            chapter_infos["name"], chapter_infos["volume"], chapter, self.forcevol
        )

        # set download path for chapter (image folder)
        chapter_path = self.manga_path / chapter_filename
        # set archive path with file format
        chapter_archive_path = Path(f"{chapter_path}{self.file_format}")

        # check if chapter already exists
        # check for folder, if file format is an empty string
        if chapter_archive_path.exists():
            if self.verbosity != "lean":
                log.warning(f"'{chapter_archive_path}' already exists. Skipping")
            # add to skipped chapters list
            return (
                {
                    "skipped": f"{chapter_infos['volume']}:{chapter_infos['chapter']}",
                    "chapter_path": None,
                }
                if self.forcevol
                else {"skipped": f"{chapter_infos['chapter']}", "chapter_path": None}
            )

        # create chapter folder (skips it if it already exists)
        chapter_path.mkdir(parents=True, exist_ok=True)

        # verbose log
        log.debug(f"Chapter UUID: {chapter_infos['uuid']}")
        log.debug(f"Filename: '{chapter_archive_path.name}'")
        log.debug(f"File path: '{chapter_archive_path}'")
        log.debug(f"Image URLS:\n{chapter_image_urls}")

        # log
        log.warning(f"Downloading: '{chapter_filename}'")

        # download images
        try:
            downloader.download_chapter(
                chapter_image_urls, chapter_path, self.download_wait
            )
        except KeyboardInterrupt:
            log.critical("Stopping")
            sys.exit(1)
        except:
            log.error(f"Cant download: '{chapter_filename}'. Skipping")
            # add to skipped chapters list
            return (
                {
                    "error": f"{chapter_infos['volume']}:{chapter_infos['chapter']}",
                    "chapter_path": None,
                }
                if self.forcevol
                else {"error": f"{chapter_infos['chapter']}", "chapter_path": None}
            )

        else:
            # Done with chapter
            log.warning(f"Successfully downloaded: '{chapter_filename}'")
            return {"chapter_path": chapter_path}

    # create an archive of the chapter if needed
    def archive_chapter(self, chapter_path: Path) -> dict:
        log.warning(f"Creating archive '{chapter_path}{self.file_format}'")
        try:
            # check if image folder is existing
            if not chapter_path.exists():
                log.error(f"Image folder: {chapter_path} does not exist")
                raise IOError
            if self.file_format == ".pdf":
                utils.make_pdf(chapter_path)
            else:
                utils.make_archive(chapter_path, self.file_format)
        except:
            log.error(f"Archive error. Skipping chapter")
            # add to skipped chapters list
            return {
                "error": chapter_path,
            }
        else:
            # remove image folder
            shutil.rmtree(chapter_path)

        return {}
