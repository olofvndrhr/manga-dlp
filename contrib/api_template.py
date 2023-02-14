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

    def __init__(self, url_uuid, language, forcevol):
        """
        get infos to initiate class
        """
        self.api_name = "Your API Name"

        self.url_uuid = url_uuid
        self.language = language
        self.forcevol = forcevol

        # attributes needed by app.py
        self.manga_uuid = "abc"
        self.manga_title = "abc"
        self.chapter_list = ["1", "2", "2.1", "5", "10"]
        self.manga_chapter_data = {  # example data
            "1": {
                "uuid": "abc",
                "volume": "1",
                "chapter": "1",
                "name": "test",
            },
            "2": {
                "uuid": "abc",
                "volume": "1",
                "chapter": "2",
                "name": "test",
            },
        }
        # or with --forcevol
        self.manga_chapter_data = {
            "1:1": {
                "uuid": "abc",
                "volume": "1",
                "chapter": "1",
                "name": "test",
            },
            "1:2": {
                "uuid": "abc",
                "volume": "1",
                "chapter": "2",
                "name": "test",
            },
        }

        def get_chapter_images(chapter: str, download_wait: float) -> list:
            """
            Get chapter images as a list (full links)

            Args:
                chapter: The chapter number (chapter data index)
                download_wait: Wait time between image downloads

            Returns:
                The list of urls of the page images
            """

            # example
            return [
                "https://abc.def/image/123.png",
                "https://abc.def/image/1234.png",
                "https://abc.def/image/12345.png",
            ]

        def create_metadata(self, chapter: str) -> dict:
            """
            Get metadata with correct keys for ComicInfo.xml
            Provide as much metadata as possible. empty/false values will be ignored

            Args:
                chapter: The chapter number (chapter data index)

            Returns:
                The metadata as a dict
            """

            # metadata types. have to be correct to be valid
            {
                "Title": str,
                "Series": str,
                "Number": str,
                "Count": int,
                "Volume": int,
                "Summary": str,
                "Genre": str,
                "Web": str,
                "PageCount": int,
                "LanguageISO": str,
                "Format": str,
                "ScanInformation": str,
                "SeriesGroup": str,
            }

            # example
            return {
                "Volume": "abc",
                "LanguageISO": "en",
                "Title": "test",
            }
