import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from loguru import logger as log

from mangadlp import downloader, utils
from mangadlp.api.mangadex import Mangadex
from mangadlp.cache import CacheDB
from mangadlp.hooks import run_hook
from mangadlp.metadata import write_metadata
from mangadlp.models import ChapterData
from mangadlp.utils import get_file_format


def match_api(url_uuid: str) -> type:
    """Match the correct api class from a string.

    Args:
        url_uuid: url/uuid to check

    Returns:
        The class of the API to use
    """
    # apis to check
    apis: List[Tuple[str, re.Pattern[str], type]] = [
        (
            "mangadex.org",
            re.compile(
                r"(mangadex.org)|([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})"
            ),
            Mangadex,
        ),
        (
            "test.org",
            re.compile(r"(test.test)"),
            type,
        ),
    ]

    # check url for match
    for api_name, api_re, api_cls in apis:
        if not api_re.search(url_uuid):
            continue
        log.info(f"API matched: {api_name}")
        return api_cls

    # no supported api found
    log.error(f"No supported api in link/uuid found: {url_uuid}")
    raise ValueError


class MangaDLP:
    """Download Mangas from supported sites.

    After initialization, start the script with the function get_manga().

    Args:
        url_uuid: URL or UUID of the manga
        language: Manga language with country codes. "en" --> english
        chapters: Chapters to download, "all" for every chapter available
        list_chapters: List all available chapters and exit
        file_format: Archive format to create. An empty string means don't archive the folder
        forcevol: Force naming of volumes. Useful for mangas where chapters reset each volume
        download_path: Download path. Defaults to '<script_dir>/downloads'
        download_wait: Time to wait for each picture to download in seconds
        manga_pre_hook_cmd: Command(s) to before after each manga
        manga_post_hook_cmd: Command(s) to run after each manga
        chapter_pre_hook_cmd: Command(s) to run before each chapter
        chapter_post_hook_cmd: Command(s) to run after each chapter
        cache_path: Path to the json cache. If emitted, no cache is used
        add_metadata: Flag to toggle creation & inclusion of metadata
    """

    def __init__(  # noqa
        self,
        url_uuid: str,
        language: str = "en",
        chapters: str = "",
        list_chapters: bool = False,
        file_format: str = "cbz",
        name_format: str = "{default}",
        name_format_none: str = "",
        forcevol: bool = False,
        download_path: Union[str, Path] = "downloads",
        download_wait: float = 0.5,
        manga_pre_hook_cmd: str = "",
        manga_post_hook_cmd: str = "",
        chapter_pre_hook_cmd: str = "",
        chapter_post_hook_cmd: str = "",
        cache_path: str = "",
        add_metadata: bool = True,
    ) -> None:
        # init parameters
        self.url_uuid = url_uuid
        self.language = language
        self.chapters = chapters
        self.list_chapters = list_chapters
        self.file_format = file_format
        self.name_format = name_format
        self.name_format_none = name_format_none
        self.forcevol = forcevol
        self.download_path: Path = Path(download_path)
        self.download_wait = download_wait
        self.manga_pre_hook_cmd = manga_pre_hook_cmd
        self.manga_post_hook_cmd = manga_post_hook_cmd
        self.chapter_pre_hook_cmd = chapter_pre_hook_cmd
        self.chapter_post_hook_cmd = chapter_post_hook_cmd
        self.cache_path = cache_path
        self.add_metadata = add_metadata
        self.hook_infos: Dict[str, Any] = {}

        # prepare everything
        self._prepare()

    def _prepare(self) -> None:
        # check and set correct file suffix/format
        self.file_format = get_file_format(self.file_format)
        # start prechecks
        self._pre_checks()
        # init api
        self.api_used = match_api(self.url_uuid)
        try:
            log.debug("Initializing api")
            self.api = self.api_used(self.url_uuid, self.language, self.forcevol)
        except Exception as exc:
            log.error("Can't initialize api. Exiting")
            raise exc
        # get manga title and uuid
        self.manga_uuid = self.api.manga_uuid
        self.manga_title = self.api.manga_title
        # get chapter list
        self.manga_chapter_list = self.api.chapter_list
        self.manga_total_chapters = len(self.manga_chapter_list)
        self.manga_path = self.download_path / self.manga_title

    def _pre_checks(self) -> None:
        # prechecks userinput/options
        # no url and no readin list given
        if not self.url_uuid:
            log.error('You need to specify a manga url/uuid with "-u" or a list with "--read"')
            raise ValueError
        # checks if --list is not used
        if not self.list_chapters:
            if not self.chapters:
                # no chapters to download were given
                log.error(
                    'You need to specify one or more chapters to download. To see all chapters use "--list"'
                )
                raise ValueError
            # if forcevol is used, but didn't specify a volume in the chapters selected
            if self.forcevol and ":" not in self.chapters:
                log.error("You need to specify the volume if you use --forcevol")
                raise ValueError
            # if forcevol is not used, but a volume is specified
            if not self.forcevol and ":" in self.chapters:
                log.error("Don't specify the volume without --forcevol")
                raise ValueError

    # once called per manga
    def get_manga(self) -> None:  # noqa
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
            chapters_to_download = utils.get_chapter_list(self.chapters, self.manga_chapter_list)

        # show chapters to download
        log.info(f"Chapters selected: {', '.join(chapters_to_download)}")
        log.info(f"{print_divider}")

        # create manga folder
        self.manga_path.mkdir(parents=True, exist_ok=True)

        # prepare cache if specified
        if self.cache_path:
            cache = CacheDB(self.cache_path, self.manga_uuid, self.language, self.manga_title)
            cached_chapters = cache.db_uuid_chapters
            log.info(f"Cached chapters: {cached_chapters}")

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
                "download_path": str(self.download_path),
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
        skipped_chapters: List[Any] = []
        error_chapters: List[Any] = []
        for chapter in chapters_to_download:
            if self.cache_path and chapter in cached_chapters:
                log.info(f"Chapter '{chapter}' is in cache. Skipping download")
                continue

            # download chapter
            try:
                chapter_path = self.get_chapter(chapter)
            except KeyboardInterrupt as exc:
                raise exc
            except FileExistsError:
                # skipping chapter download as its already available
                skipped_chapters.append(chapter)
                # update cache
                if self.cache_path:
                    cache.add_chapter(chapter)
                continue
            except Exception:
                # skip download/packing due to an error
                error_chapters.append(chapter)
                continue

            # add metadata
            if self.add_metadata:
                try:
                    metadata = self.api.create_metadata(chapter)
                    write_metadata(
                        chapter_path,
                        {"Format": self.file_format[1:], **metadata},
                    )
                except Exception as exc:
                    log.warning(f"Can't write metadata for chapter '{chapter}'. Reason={exc}")

            # pack downloaded folder
            if self.file_format:
                try:
                    self.archive_chapter(chapter_path)
                except Exception:
                    error_chapters.append(chapter)
                    continue

            # done with chapter
            log.info(f"Done with chapter '{chapter}'")

            # update cache
            if self.cache_path:
                cache.add_chapter(chapter)

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
    def get_chapter(self, chapter: str) -> Path:
        # get chapter infos
        chapter_infos: ChapterData = self.api.manga_chapter_data[chapter]
        log.debug(f"Chapter infos: {chapter_infos}")

        # get image urls for chapter
        try:
            chapter_image_urls = self.api.get_chapter_images(chapter, self.download_wait)
        except KeyboardInterrupt as exc:
            log.critical("Keyboard interrupt. Stopping")
            raise exc

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

            # error
            raise SystemError

        # get filename for chapter (without suffix)
        chapter_filename = utils.get_filename(
            self.manga_title,
            chapter_infos["name"],
            chapter_infos["volume"],
            chapter,
            self.forcevol,
            self.name_format,
            self.name_format_none,
        )
        log.debug(f"Filename: '{chapter_filename}'")

        # set download path for chapter (image folder)
        chapter_path: Path = self.manga_path / chapter_filename
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

            # skipped
            raise FileExistsError

        # create chapter folder (skips it if it already exists)
        chapter_path.mkdir(parents=True, exist_ok=True)

        # verbose log
        log.debug(f"Chapter UUID: {chapter_infos['uuid']}")
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
            downloader.download_chapter(chapter_image_urls, chapter_path, self.download_wait)
        except KeyboardInterrupt as exc:
            log.critical("Keyboard interrupt. Stopping")
            raise exc
        except Exception as exc:
            log.error(f"Cant download: '{chapter_filename}'. Skipping")

            # run chapter post hook
            run_hook(
                command=self.chapter_post_hook_cmd,
                hook_type="chapter_post",
                status="starting",
                reason="Download error",
                **self.hook_infos,
            )

            # chapter error
            raise exc

        # Done with chapter
        log.info(f"Successfully downloaded: '{chapter_filename}'")

        # ok
        return chapter_path

    # create an archive of the chapter if needed
    def archive_chapter(self, chapter_path: Path) -> None:
        log.info(f"Creating archive '{chapter_path}{self.file_format}'")
        try:
            # check if image folder is existing
            if not chapter_path.exists():
                log.error(f"Image folder: {chapter_path} does not exist")
                raise OSError
            if self.file_format == ".pdf":
                utils.make_pdf(chapter_path)
            else:
                utils.make_archive(chapter_path, self.file_format)
        except Exception as exc:
            log.error("Archive error. Skipping chapter")
            raise exc

        # remove image folder
        shutil.rmtree(chapter_path)
