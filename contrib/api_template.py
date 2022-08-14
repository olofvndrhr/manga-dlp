# api template for manga-dlp


class YourAPI:
    """Your API Class.
    Get infos for a manga from example.org

    Args:
        url_uuid (str): URL or UUID of the manga
        language (str): Manga language with country codes. "en" --> english
        forcevol (bool): Force naming of volumes. Useful for mangas where chapters reset each volume

    Attributes:
        api_name (str): Name of the API
        manga_uuid (str): UUID of the manga, without the url part
        manga_title (str): The title of the manga, sanitized for all filesystems
        chapter_list (list): A list of all available chapters for the language

    """

    # api information - example
    api_base_url = "https://api.mangadex.org"
    img_base_url = "https://uploads.mangadex.org"

    # get infos to initiate class
    def __init__(self, url_uuid, language, forcevol):
        # static info
        self.api_name = "Your API Name"

        self.url_uuid = url_uuid
        self.language = language
        self.forcevol = forcevol

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
