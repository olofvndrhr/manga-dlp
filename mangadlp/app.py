import re
import shutil
import sys
from pathlib import Path
from typing import Any

from loguru import logger as log

from mangadlp import downloader, utils
from mangadlp.api.mangadex import Mangadex
from mangadlp.hooks import run_hook


class MangaDLP:
    """Download Mangas from supported sites.
    After initialization, start the script with the function get_manga().

    Args:
        url_uuid (str): URL or UUID of the manga
        language (str): Manga language with country codes. "en" --> english
        chapters (str): Chapters to download, "all" for every chapter available
        list_chapters (bool): List all available chapters and exit
        file_format (str): Archive format to create. An empty string means don't archive the folder
        forcevol (bool): Force naming of volumes. Useful for mangas where chapters reset each volume
        download_path (str): Download path. Defaults to '<script_dir>/downloads'
        download_wait (float): Time to wait for each picture to download in seconds

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
        manga_pre_hook_cmd: str = "",
        manga_post_hook_cmd: str = "",
        chapter_pre_hook_cmd: str = "",
        chapter_post_hook_cmd: str = "",
    ) -> None:
        # init parameters
        self.url_uuid: str = url_uuid
        self.language: str = language
        self.chapters: str = chapters
        self.list_chapters: bool = list_chapters
        self.file_format: str = file_format
        self.forcevol: bool = forcevol
        self.download_path: str = download_path
        self.download_wait: float = download_wait
        self.manga_pre_hook_cmd: str = manga_pre_hook_cmd
        self.manga_post_hook_cmd: str = manga_post_hook_cmd
        self.chapter_pre_hook_cmd: str = chapter_pre_hook_cmd
        self.chapter_post_hook_cmd: str = chapter_post_hook_cmd
        self.hook_infos: dict = {}

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
        self.manga_total_chapters = len(self.manga_chapter_list)
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
        sys.exit(1)

    # once called per manga
    def get_manga(self) -> None:
        # create empty skipped chapters list
        skipped_chapters: list[Any] = []
        error_chapters: list[Any] = []

        print_divider = "========================================="
        # show infos
        log.info(f"{print_divider}")
        log.info(f"Manga Name: {self.manga_title}")
        log.info(f"Manga UUID: {self.manga_uuid}")
        log.info(f"Total chapters: {self.manga_total_chapters}")

        # list chapters if list_chapters is true
        if self.list_chapters:
            log.info(f"Available Chapters: {', '.join(self.manga_chapter_list)}")
            log.info(f"{print_divider}\n")
            return

        # check chapters to download if not all
        if self.chapters.lower() == "all":
            chapters_to_download = self.manga_chapter_list
        else:
            chapters_to_download = utils.get_chapter_list(
                self.chapters, self.manga_chapter_list
            )

        # show chapters to download
        log.info(f"Chapters selected: {', '.join(chapters_to_download)}")
        log.info(f"{print_divider}")

        # create manga folder
        self.manga_path.mkdir(parents=True, exist_ok=True)

        # create dict with all variables for the hooks
        self.hook_infos.update(
            {
                "api": self.api.api_name,
                "manga_url_uuid": self.url_uuid,
                "manga_uuid": self.manga_uuid,
                "manga_title": self.manga_title,
                "language": self.language,
                "total_chapters": self.manga_total_chapters,
                "chapters_to_download": chapters_to_download,
                "file_format": self.file_format,
                "forcevol": self.forcevol,
                "download_path": self.download_path,
                "manga_path": self.manga_path,
            }
        )

        # start manga pre hook
        run_hook(
            command=self.manga_pre_hook_cmd,
            hook_type="manga_pre",
            status="starting",
            **self.hook_infos,
        )

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

                # start chapter post hook
                run_hook(
                    command=self.chapter_post_hook_cmd,
                    hook_type="chapter_post",
                    status="successful",
                    **self.hook_infos,
                )

        # done with manga
        log.info(f"{print_divider}")
        log.info(f"Done with manga: {self.manga_title}")

        # filter skipped list
        skipped_chapters = list(filter(None, skipped_chapters))
        if len(skipped_chapters) >= 1:
            log.info(f"Skipped chapters: {', '.join(skipped_chapters)}")

        # filter error list
        error_chapters = list(filter(None, error_chapters))
        if len(error_chapters) >= 1:
            log.info(f"Chapters with errors: {', '.join(error_chapters)}")

        # start manga post hook
        run_hook(
            command=self.manga_post_hook_cmd,
            hook_type="manga_post",
            status="successful",
            **self.hook_infos,
        )

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

            run_hook(
                command=self.chapter_pre_hook_cmd,
                hook_type="chapter_pre",
                status="skipped",
                reason="No images",
                **self.hook_infos,
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
            log.info(f"'{chapter_archive_path}' already exists. Skipping")

            run_hook(
                command=self.chapter_pre_hook_cmd,
                hook_type="chapter_pre",
                status="skipped",
                reason="Existing",
                **self.hook_infos,
            )

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

        # create dict with all variables for the hooks
        self.hook_infos.update(
            {
                "chapter_filename": chapter_filename,
                "chapter_path": chapter_path,
                "chapter_archive_path": chapter_archive_path,
                "chapter_uuid": chapter_infos["uuid"],
                "chapter_volume": chapter_infos["volume"],
                "chapter_number": chapter_infos["chapter"],
                "chapter_name": chapter_infos["name"],
            }
        )

        # start chapter pre hook
        run_hook(
            command=self.chapter_pre_hook_cmd,
            hook_type="chapter_pre",
            status="starting",
            **self.hook_infos,
        )

        # log
        log.info(f"Downloading: '{chapter_filename}'")

        # download images
        try:
            downloader.download_chapter(
                chapter_image_urls, chapter_path, self.download_wait
            )
        except KeyboardInterrupt:
            log.critical("Stopping")
            sys.exit(1)
        except Exception:
            log.error(f"Cant download: '{chapter_filename}'. Skipping")

            # run chapter post hook
            run_hook(
                command=self.chapter_post_hook_cmd,
                hook_type="chapter_post",
                status="starting",
                reason="Download error",
                **self.hook_infos,
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

        else:
            # Done with chapter
            log.info(f"Successfully downloaded: '{chapter_filename}'")

            return {"chapter_path": chapter_path}

    # create an archive of the chapter if needed
    def archive_chapter(self, chapter_path: Path) -> dict:
        log.info(f"Creating archive '{chapter_path}{self.file_format}'")
        try:
            # check if image folder is existing
            if not chapter_path.exists():
                log.error(f"Image folder: {chapter_path} does not exist")
                raise IOError
            if self.file_format == ".pdf":
                utils.make_pdf(chapter_path)
            else:
                utils.make_archive(chapter_path, self.file_format)
        except Exception:
            log.error("Archive error. Skipping chapter")
            # add to skipped chapters list
            return {
                "error": chapter_path,
            }
        else:
            # remove image folder
            shutil.rmtree(chapter_path)

        return {}
