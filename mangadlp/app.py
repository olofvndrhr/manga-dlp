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
    :param verbosity: Verbosity of the output

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
        verbosity: str = "normal",
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
        # prepare logger
        if self.verbosity == "lean":
            logging.getLogger().setLevel(25)
        elif self.verbosity == "verbose":
            logging.getLogger().setLevel(15)
        elif self.verbosity == "debug":
            logging.getLogger().setLevel(10)
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
            logging.error(
                'You need to specify a manga url/uuid with "-u" or a list with "--read"'
            )
            sys.exit(1)
        # checks if --list is not used
        if not self.list_chapters:
            if self.chapters is None:
                # no chapters to download were given
                logging.error(
                    'You need to specify one or more chapters to download. To see all chapters use "--list"'
                )
                sys.exit(1)
            # if forcevol is used, but didn't specify a volume in the chapters selected
            if self.forcevol and ":" not in self.chapters:
                logging.error("You need to specify the volume if you use --forcevol")
                sys.exit(1)
            # if forcevol is not used, but a volume is specified
            if not self.forcevol and ":" in self.chapters:
                logging.error("Don't specify the volume without --forcevol")
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
            logging.critical("Not supported yet")
            sys.exit(1)

        # no supported api found
        logging.error(f"No supported api in link/uuid found: {url_uuid}")
        raise ValueError

    # once called per manga
    def get_manga(self) -> None:
        # create empty skipped chapters list
        skipped_chapters: list[Any] = []
        error_chapters: list[Any] = []

        print_divider = "========================================="
        # show infos
        logging.info(f"{print_divider}")
        logging.lean(f"Manga Name: {self.manga_title}")  # type: ignore
        logging.info(f"Manga UUID: {self.manga_uuid}")
        logging.info(f"Total chapters: {len(self.manga_chapter_list)}")

        # list chapters if list_chapters is true
        if self.list_chapters:
            logging.info(f"Available Chapters: {', '.join(self.manga_chapter_list)}")
            logging.info(f"{print_divider}\n")
            return None

        # check chapters to download if not all
        if self.chapters.lower() == "all":
            chapters_to_download = self.manga_chapter_list
        else:
            chapters_to_download = utils.get_chapter_list(
                self.chapters, self.manga_chapter_list
            )

        # show chapters to download
        logging.lean(f"Chapters selected: {', '.join(chapters_to_download)}")  # type: ignore
        logging.info(f"{print_divider}")

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
                logging.info("Done with chapter\n")

        # done with manga
        logging.info(f"{print_divider}")
        logging.lean(f"Done with manga: {self.manga_title}")  # type: ignore
        # filter skipped list
        skipped_chapters = list(filter(None, skipped_chapters))
        if len(skipped_chapters) >= 1:
            logging.lean(f"Skipped chapters: {', '.join(skipped_chapters)}")  # type: ignore
        # filter error list
        error_chapters = list(filter(None, error_chapters))
        if len(error_chapters) >= 1:
            logging.lean(f"Chapters with errors: {', '.join(error_chapters)}")  # type: ignore

        logging.info(f"{print_divider}\n")

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
            logging.critical("Stopping")
            sys.exit(1)

        # check if the image urls are empty. if yes skip this chapter (for mass downloads)
        if not chapter_image_urls:
            logging.error(
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
                logging.warning(f"'{chapter_archive_path}' already exists. Skipping")
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
        logging.verbose(f"Chapter UUID: {chapter_infos['uuid']}")  # type: ignore
        logging.verbose(f"Filename: '{chapter_archive_path.name}'")  # type: ignore
        logging.verbose(f"File path: '{chapter_archive_path}'")  # type: ignore
        logging.verbose(f"Image URLS:\n{chapter_image_urls}")  # type: ignore

        # log
        logging.lean(f"Downloading: '{chapter_filename}'")  # type: ignore

        # download images
        try:
            downloader.download_chapter(
                chapter_image_urls, chapter_path, self.download_wait
            )
        except KeyboardInterrupt:
            logging.critical("Stopping")
            sys.exit(1)
        except:
            logging.error(f"Cant download: '{chapter_filename}'. Skipping")
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
            logging.lean(f"INFO: Successfully downloaded: '{chapter_filename}'")  # type: ignore
            return {"chapter_path": chapter_path}

    # create an archive of the chapter if needed
    def archive_chapter(self, chapter_path: Path) -> dict:
        logging.lean(f"INFO: Creating '{self.file_format}' archive")  # type: ignore
        try:
            # check if image folder is existing
            if not chapter_path.exists():
                logging.error(f"Image folder: {chapter_path} does not exist")
                raise IOError
            if self.file_format == ".pdf":
                utils.make_pdf(chapter_path)
            else:
                utils.make_archive(chapter_path, self.file_format)
        except:
            logging.error(f"Archive error. Skipping chapter")
            # add to skipped chapters list
            return {
                "error": chapter_path,
            }
        else:
            # remove image folder
            shutil.rmtree(chapter_path)

        return {}
