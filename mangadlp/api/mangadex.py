import requests
import re
import mangadlp.utils as utils


class Mangadex:

    # api information
    api_base_url = "https://api.mangadex.org"
    img_base_url = "https://uploads.mangadex.org"
    # get infos to initiate class

    def __init__(self, manga_url, manga_lang):
        # static info
        self.manga_url = manga_url
        self.manga_lang = manga_lang

        # infos from functions
        self.manga_uuid = self.get_manga_uuid()
        self.manga_title = self.get_manga_title()
        self.manga_chapter_data = self.get_chapter_data()

    # get the uuid for the manga
    def get_manga_uuid(self):
        # isolate id from url
        uuid_regex = re.compile(
            "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
        )
        # check for new mangadex id
        if uuid_regex.search(self.manga_url):
            manga_uuid = uuid_regex.search(self.manga_url)[0]
        else:
            print("No valid uuid found")
            exit(1)
        # check if the manga exists
        try:
            req = requests.get(f"{self.api_base_url}/manga/{manga_uuid}")
        except:
            print("Error. Maybe the MangaDex API is down?")
            exit(1)
        else:
            # check mangadex status
            response = req.json()["result"]
            if not response == "ok":
                print("Manga not found")
                exit(1)

        return manga_uuid

    # get the title of the manga (and fix the filename)
    def get_manga_title(self):
        req = requests.get(f"{self.api_base_url}/manga/{self.manga_uuid}")
        api_resp = req.json()
        try:
            title = api_resp["data"]["attributes"]["title"][self.manga_lang]
        except:
            # search in alt titles
            try:
                alt_titles = {}
                for title in api_resp["data"]["attributes"]["altTitles"]:
                    alt_titles.update(title)
                title = alt_titles[self.manga_lang]
            except:  # no title on requested language found
                print("Chapter in requested language not found.")
                exit(1)

        return utils.fix_name(title)

    # get chapter data like name, uuid etc
    def get_chapter_data(self):
        content_ratings = "contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic"
        chap_data_list = []
        req = requests.get(
            f"{self.api_base_url}/manga/{self.manga_uuid}/feed?limit=0&translatedLanguage[]={self.manga_lang}&{content_ratings}"
        )
        try:
            total = req.json()["total"]
        except:
            print(
                "Error retrieving the chapters list. Did you specify a valid language code?"
            )
            exit(1)
        if total == 0:
            print("No chapters available to download!")
            exit(0)
        last_chap = ["", ""]
        offset = 0
        while offset < total:  # if more than 500 chapters
            req = requests.get(
                f"{self.api_base_url}/manga/{self.manga_uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={self.manga_lang}&offset={offset}&{content_ratings}"
            )
            for chapter in req.json()["data"]:
                # chapter infos from feed
                chap_num = chapter["attributes"]["chapter"]
                chap_vol = chapter["attributes"]["volume"]
                chap_uuid = chapter["id"]
                chap_name = chapter["attributes"]["title"]
                if chap_name is not None:
                    chap_name = utils.fix_name(chap_name)
                # check if the chapter is external (can't download them)
                chap_external = chapter["attributes"]["externalUrl"]
                # name chapter "oneshot" if there is no chapter number
                if chap_external is None and chap_num is None:
                    # check for duplicates
                    if last_chap[0] == chap_vol and last_chap[1] == chap_num:
                        continue
                    chap_data_list.append([chap_vol, "Oneshot", chap_uuid, chap_name])
                # else add chapter number
                elif chap_external is None:
                    # check for duplicates
                    if last_chap[0] == chap_vol and last_chap[1] == chap_num:
                        continue
                    chap_data_list.append([chap_vol, chap_num, chap_uuid, chap_name])
                last_chap = [chap_vol, chap_num]
            offset += 500

        return chap_data_list

    # TODO
    # get images for the chapter (mangadex@home)
    def get_chapter_data(self, chapter_uuid):
        athome_url = f"{self.api_base_url}/at-home/server"
        r = requests.get(f"{athome_url}/{chapter_uuid}")
        chap_hash = r.json()["chapter"]["hash"]
        chap_data = r.json()["chapter"]["data"]

        return chap_hash, chap_data

    # get index of chapter
    def get_chapter_index(self, chapter, forcevol):
        if forcevol:
            chapter_index = next(
                c for c in self.manga_chapter_data if f"{c[0]}:{c[1]}" == chapter
            )
        else:
            chapter_index = next(c for c in self.manga_chapter_data if c[1] == chapter)

        return chapter_index

    # create list of chapters
    def create_chapter_list(self, chapter_data, forcevol):
        chapter_list = []
        for chap in chapter_data:
            volume_number = chap[0]
            chapter_number = chap[1]
            if forcevol:
                chapter_list.append(f"{volume_number}:{chapter_number}")
            else:
                chapter_list.append(chapter_number)

        return chapter_list

    # move the mangadex@home
    # get list of image urls
    def get_img_urls(self, images, chapter_hash):
        img_urls = []
        for img in images:
            img_urls.append(f"{self.img_base_url}/data/{chapter_hash}/{img}")

        return img_urls
