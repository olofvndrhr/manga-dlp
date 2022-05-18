# api template for manga-dlp


class YourAPI:
    # api information - example
    api_base_url = "https://api.mangadex.org"
    img_base_url = "https://uploads.mangadex.org"

    # get infos to initiate class
    def __init__(self, url_uuid, language, forcevol, verbose):
        # static info
        self.url_uuid = url_uuid
        self.language = language
        self.forcevol = forcevol
        self.verbose = verbose

        # attributes needed by app.py
        self.manga_uuid = "abc"
        self.manga_title = "abc"
        self.chapter_list = "abc"

        # methods needed by app.py
        # get chapter infos as a dictionary
        def get_chapter_infos(chapter: str) -> dict:
            # these keys have to be returned
            return {
                "uuid": chapter_uuid,
                "volume": chapter_vol,
                "chapter": chapter_num,
                "name": chapter_name,
            }

        # get chapter images as a list (full links)
        def get_chapter_images(chapter: str, download_wait: float) -> list:
            # example
            return [
                "https://abc.def/image/123.png",
                "https://abc.def/image/1234.png",
                "https://abc.def/image/12345.png",
            ]
