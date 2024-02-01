import re
from time import sleep
from typing import Any, Dict, List

import requests
from loguru import logger as log

from mangadlp import utils
from mangadlp.models import ChapterData, ComicInfo


class Mangadex:
    """Mangadex API Class.

    Get infos for a manga from mangadex.org.

    Args:
        url_uuid (str): URL or UUID of the manga
        language (str): Manga language with country codes. "en" --> english
        forcevol (bool): Force naming of volumes. Useful for mangas where chapters reset each volume

    Attributes:
        api_name (str): Name of the API
        manga_uuid (str): UUID of the manga, without the url part
        manga_data (dict): Infos of the manga. Name, title etc.
        manga_title (str): The title of the manga, sanitized for all file systems
        manga_chapter_data (dict): All chapter data of the manga. Volumes, chapters, chapter uuids and chapter names
        chapter_list (list): A list of all available chapters for the language

    """

    # api information
    api_base_url = "https://api.mangadex.org"
    img_base_url = "https://uploads.mangadex.org"

    # get infos to initiate class
    def __init__(self, url_uuid: str, language: str, forcevol: bool):
        # static info
        self.api_name = "Mangadex"

        self.url_uuid = url_uuid
        self.language = language
        self.forcevol = forcevol

        # api stuff
        self.api_content_ratings = "contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic"
        self.api_language = f"translatedLanguage[]={self.language}"
        self.api_additions = f"{self.api_language}&{self.api_content_ratings}"

        # infos from functions
        self.manga_uuid = self.get_manga_uuid()
        self.manga_data = self.get_manga_data()
        self.manga_title = self.get_manga_title()
        self.manga_chapter_data = self.get_chapter_data()
        self.chapter_list = self.create_chapter_list()

    # get the uuid for the manga
    def get_manga_uuid(self) -> str:
        # isolate id from url
        uuid_regex = re.compile("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}")
        # try to get uuid in string
        try:
            uuid = uuid_regex.search(self.url_uuid)[0]  # type: ignore
        except Exception as exc:
            log.error("No valid UUID found")
            raise exc

        return uuid

    # make initial request
    def get_manga_data(self) -> Dict[str, Any]:
        log.debug(f"Getting manga data for: {self.manga_uuid}")
        counter = 1
        while counter <= 3:
            try:
                response = requests.get(f"{self.api_base_url}/manga/{self.manga_uuid}", timeout=10)
            except Exception as exc:
                if counter >= 3:
                    log.error("Maybe the MangaDex API is down?")
                    raise exc
                log.error("Mangadex API not reachable. Retrying")
                sleep(2)
                counter += 1
            else:
                break

        response_body: Dict[str, Dict[str, Any]] = response.json()
        # check if manga exists
        if response_body["result"] != "ok":
            log.error("Manga not found")
            raise KeyError

        return response_body["data"]

    # get the title of the manga (and fix the filename)
    def get_manga_title(self) -> str:
        log.debug(f"Getting manga title for: {self.manga_uuid}")
        attributes = self.manga_data["attributes"]
        # try to get the title in requested language
        try:
            found_title = attributes["title"][self.language]
            title = utils.fix_name(found_title)
        except KeyError:
            log.info("Manga title not found in requested language. Trying alt titles")
        else:
            log.debug(f"Language={self.language}, Title='{title}'")
            return title  # type: ignore

        # search in alt titles
        try:
            log.debug(f"Alt titles: {attributes['altTitles']}")
            for item in attributes["altTitles"]:
                if item.get(self.language):
                    alt_title_item = item
                    break
            found_title = alt_title_item[self.language]
        except (KeyError, UnboundLocalError):
            log.warning("Manga title also not found in alt titles. Falling back to english title")
        else:
            title = utils.fix_name(found_title)
            log.debug(f"Language={self.language}, Alt-title='{found_title}'")
            return title  # type: ignore

        found_title = attributes["title"]["en"]
        title = utils.fix_name(found_title)

        log.debug(f"Language=en, Fallback-title='{title}'")

        return title  # type: ignore

    # check if chapters are available in requested language
    def check_chapter_lang(self) -> int:
        log.debug(f"Checking for chapters in specified language for: {self.manga_uuid}")
        r = requests.get(
            f"{self.api_base_url}/manga/{self.manga_uuid}/feed?limit=0&{self.api_additions}",
            timeout=10,
        )
        try:
            total_chapters: int = r.json()["total"]
        except Exception as exc:
            log.error("Error retrieving the chapters list. Did you specify a valid language code?")
            raise exc
        if total_chapters == 0:
            log.error("No chapters available to download in specified language")
            raise KeyError

        log.debug(f"Total chapters={total_chapters}")
        return total_chapters

    # get chapter data like name, uuid etc
    def get_chapter_data(self) -> Dict[str, ChapterData]:
        log.debug(f"Getting chapter data for: {self.manga_uuid}")
        api_sorting = "order[chapter]=asc&order[volume]=asc"
        # check for chapters in specified lang
        total_chapters = self.check_chapter_lang()

        chapter_data: Dict[str, ChapterData] = {}
        last_volume, last_chapter = ("", "")
        offset = 0
        while offset < total_chapters:  # if more than 500 chapters
            r = requests.get(
                f"{self.api_base_url}/manga/{self.manga_uuid}/feed?{api_sorting}&limit=500&offset={offset}&{self.api_additions}",
                timeout=10,
            )
            response_body: Dict[str, Any] = r.json()
            for chapter in response_body["data"]:
                attributes: Dict[str, Any] = chapter["attributes"]
                # chapter infos from feed
                chapter_num: str = attributes.get("chapter") or ""
                chapter_vol: str = attributes.get("volume") or ""
                chapter_uuid: str = chapter.get("id") or ""
                chapter_name: str = attributes.get("title") or ""
                chapter_external: str = attributes.get("externalUrl") or ""
                chapter_pages: int = attributes.get("pages") or 0

                # check for chapter title and fix it
                if chapter_name:
                    chapter_name = utils.fix_name(chapter_name)

                # check if the chapter is external (can't download them)
                if chapter_external:
                    log.debug(f"Chapter is external. Skipping: {chapter_name}")
                    continue

                # check if its duplicate from the last entry
                if last_volume == chapter_vol and last_chapter == chapter_num:
                    continue

                # export chapter data as a dict
                chapter_index = chapter_num if not self.forcevol else f"{chapter_vol}:{chapter_num}"
                chapter_data[chapter_index] = {
                    "uuid": chapter_uuid,
                    "volume": chapter_vol,
                    "chapter": chapter_num,
                    "name": chapter_name,
                    "pages": chapter_pages,
                }
                # add last chapter to duplicate check
                last_volume, last_chapter = (chapter_vol, chapter_num)

            # increase offset for mangas with more than 500 chapters
            offset += 500

        return chapter_data

    # get images for the chapter (mangadex@home)
    def get_chapter_images(self, chapter: str, wait_time: float) -> List[str]:
        log.debug(f"Getting chapter images for: {self.manga_uuid}")
        athome_url = f"{self.api_base_url}/at-home/server"
        chapter_uuid = self.manga_chapter_data[chapter]["uuid"]

        # retry up to two times if the api applied rate limits
        api_error = False
        counter = 1
        while counter <= 3:
            try:
                r = requests.get(f"{athome_url}/{chapter_uuid}", timeout=10)
                api_data = r.json()
                if api_data["result"] != "ok":
                    log.error(f"No chapter with the id {chapter_uuid} found")
                    api_error = True
                    raise IndexError
                if api_data["chapter"]["data"] is None:
                    log.error(f"No chapter data found for chapter {chapter_uuid}")
                    api_error = True
                    raise IndexError
                # no error
                api_error = False
                break
            except Exception:
                if counter >= 3:
                    api_error = True
                log.error("Retrying in a few seconds")
                counter += 1
                sleep(wait_time + 2)
        # check if result is ok
        else:
            if api_error:
                return []

        chapter_hash = api_data["chapter"]["hash"]
        chapter_img_data = api_data["chapter"]["data"]

        # get list of image urls
        image_urls: List[str] = []
        for image in chapter_img_data:
            image_urls.append(f"{self.img_base_url}/data/{chapter_hash}/{image}")

        sleep(wait_time)

        return image_urls

    # create list of chapters
    def create_chapter_list(self) -> List[str]:
        log.debug(f"Creating chapter list for: {self.manga_uuid}")
        chapter_list: List[str] = []
        for data in self.manga_chapter_data.values():
            chapter_number: str = data["chapter"]
            volume_number: str = data["volume"]
            if self.forcevol:
                chapter_list.append(f"{volume_number}:{chapter_number}")
            else:
                chapter_list.append(chapter_number)

        return chapter_list

    def create_metadata(self, chapter: str) -> ComicInfo:
        log.info("Creating metadata from api")

        chapter_data = self.manga_chapter_data[chapter]
        try:
            volume = int(chapter_data["volume"])
        except (ValueError, TypeError):
            volume = None
        metadata: ComicInfo = {
            "Volume": volume,
            "Number": chapter_data.get("chapter"),
            "PageCount": chapter_data.get("pages"),
            "Title": chapter_data.get("name"),
            "Series": self.manga_title,
            "Count": len(self.manga_chapter_data),
            "LanguageISO": self.language,
            "Summary": self.manga_data["attributes"]["description"].get("en"),
            "Genre": self.manga_data["attributes"].get("publicationDemographic"),
            "Web": f"https://mangadex.org/title/{self.manga_uuid}",
        }

        return metadata
