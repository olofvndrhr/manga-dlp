import re
import sys
from time import sleep

import requests
from loguru import logger as log

from mangadlp import utils


class Mangadex:
    """Mangadex API Class.
    Get infos for a manga from mangadex.org

    Args:
        url_uuid (str): URL or UUID of the manga
        language (str): Manga language with country codes. "en" --> english
        forcevol (bool): Force naming of volumes. Useful for mangas where chapters reset each volume

    Attributes:
        api_name (str): Name of the API
        manga_uuid (str): UUID of the manga, without the url part
        manga_data (dict): Infos of the manga. Name, title etc
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

    # make initial request
    def get_manga_data(self) -> dict:
        log.debug(f"Getting manga data for: {self.manga_uuid}")
        counter = 1
        while counter <= 3:
            try:
                manga_data = requests.get(
                    f"{self.api_base_url}/manga/{self.manga_uuid}"
                )
            except Exception:
                if counter >= 3:
                    log.error("Maybe the MangaDex API is down?")
                    sys.exit(1)
                else:
                    log.error("Mangadex API not reachable. Retrying")
                    sleep(2)
                    counter += 1
            else:
                break
        # check if manga exists
        if manga_data.json()["result"] != "ok":
            log.error("Manga not found")
            sys.exit(1)

        return manga_data.json()

    # get the uuid for the manga
    def get_manga_uuid(self) -> str:
        # isolate id from url
        uuid_regex = re.compile(
            "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
        )
        # try to get uuid in string
        try:
            uuid = uuid_regex.search(self.url_uuid)[0]  # type: ignore
        except Exception:
            log.error("No valid UUID found")
            sys.exit(1)

        return uuid

    # get the title of the manga (and fix the filename)
    def get_manga_title(self) -> str:
        log.debug(f"Getting manga title for: {self.manga_uuid}")
        manga_data = self.manga_data
        try:
            title = manga_data["data"]["attributes"]["title"][self.language]
        except Exception:
            # search in alt titles
            try:
                alt_titles = {}
                for title in manga_data["data"]["attributes"]["altTitles"]:
                    alt_titles.update(title)
                title = alt_titles[self.language]
            except Exception:  # no title on requested language found
                log.error("Chapter in requested language not found.")
                sys.exit(1)

        return utils.fix_name(title)

    # check if chapters are available in requested language
    def check_chapter_lang(self) -> int:
        log.debug(f"Checking for chapters in specified language for: {self.manga_uuid}")
        r = requests.get(
            f"{self.api_base_url}/manga/{self.manga_uuid}/feed?limit=0&{self.api_additions}"
        )
        try:
            total_chapters = r.json()["total"]
        except Exception:
            log.error(
                "Error retrieving the chapters list. Did you specify a valid language code?"
            )
            return 0
        else:
            if total_chapters == 0:
                log.error("No chapters available to download!")
                return 0

        return total_chapters

    # get chapter data like name, uuid etc
    def get_chapter_data(self) -> dict:
        log.debug(f"Getting chapter data for: {self.manga_uuid}")
        api_sorting = "order[chapter]=asc&order[volume]=asc"
        # check for chapters in specified lang
        total_chapters = self.check_chapter_lang()
        if total_chapters == 0:
            sys.exit(1)

        chapter_data = {}
        last_chapter = ["", ""]
        offset = 0
        while offset < total_chapters:  # if more than 500 chapters
            r = requests.get(
                f"{self.api_base_url}/manga/{self.manga_uuid}/feed?{api_sorting}&limit=500&offset={offset}&{self.api_additions}"
            )
            for chapter in r.json()["data"]:
                # chapter infos from feed
                chapter_num = chapter["attributes"]["chapter"]
                chapter_vol = chapter["attributes"]["volume"]
                chapter_uuid = chapter["id"]
                chapter_name = chapter["attributes"]["title"]
                chapter_external = chapter["attributes"]["externalUrl"]

                # check for chapter title and fix it
                if chapter_name is None:
                    chapter_name = "No Title"
                else:
                    chapter_name = utils.fix_name(chapter_name)
                # check if the chapter is external (can't download them)
                if chapter_external is not None:
                    continue
                # name chapter "oneshot" if there is no chapter number
                if chapter_num is None:
                    chapter_num = "Oneshot"

                # check if its duplicate from the last entry
                if last_chapter[0] == chapter_vol and last_chapter[1] == chapter_num:
                    continue

                # export chapter data as a dict
                chapter_index = (
                    chapter_num if not self.forcevol else f"{chapter_vol}:{chapter_num}"
                )
                chapter_data[chapter_index] = [
                    chapter_uuid,
                    chapter_vol,
                    chapter_num,
                    chapter_name,
                ]
                # add last chapter to duplicate check
                last_chapter = [chapter_vol, chapter_num]

            # increase offset for mangas with more than 500 chapters
            offset += 500

        return chapter_data

    # get images for the chapter (mangadex@home)
    def get_chapter_images(self, chapter: str, wait_time: float) -> list:
        log.debug(f"Getting chapter images for: {self.manga_uuid}")
        athome_url = f"{self.api_base_url}/at-home/server"
        chapter_uuid = self.manga_chapter_data[chapter][0]

        # retry up to two times if the api applied rate limits
        api_error = False
        counter = 1
        while counter <= 3:
            try:
                r = requests.get(f"{athome_url}/{chapter_uuid}")
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
        image_urls = []
        for image in chapter_img_data:
            image_urls.append(f"{self.img_base_url}/data/{chapter_hash}/{image}")

        sleep(wait_time)

        return image_urls

    # create list of chapters
    def create_chapter_list(self) -> list:
        log.debug(f"Creating chapter list for: {self.manga_uuid}")
        chapter_list = []
        for chapter in self.manga_chapter_data.items():
            chapter_info = self.get_chapter_infos(chapter[0])
            chapter_number = chapter_info["chapter"]
            volume_number = chapter_info["volume"]
            if self.forcevol:
                chapter_list.append(f"{volume_number}:{chapter_number}")
            else:
                chapter_list.append(chapter_number)

        return chapter_list

    # create easy to access chapter infos
    def get_chapter_infos(self, chapter: str) -> dict:
        log.debug(f"Getting chapter infos for: {self.manga_chapter_data[chapter][0]}")
        chapter_uuid = self.manga_chapter_data[chapter][0]
        chapter_vol = self.manga_chapter_data[chapter][1]
        chapter_num = self.manga_chapter_data[chapter][2]
        chapter_name = self.manga_chapter_data[chapter][3]

        return {
            "uuid": chapter_uuid,
            "volume": chapter_vol,
            "chapter": chapter_num,
            "name": chapter_name,
        }
