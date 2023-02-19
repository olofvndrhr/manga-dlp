from typing import List, Dict, Union

# api template for manga-dlp


class YourAPI:
    """Your API Class.

    Get infos for a manga from example.org.

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

    def __init__(self, url_uuid: str, language: str, forcevol: bool):
        """get infos to initiate class."""
        self.api_name = "Your API Name"

        self.url_uuid = url_uuid
        self.language = language
        self.forcevol = forcevol

        # attributes needed by app.py
        self.manga_uuid = "abc"
        self.manga_title = "abc"
        self.chapter_list = ["1", "2", "2.1", "5", "10"]
        self.manga_chapter_data: Dict[
            str, Dict[str, Union[str, int]]
        ] = {  # example data
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
        self.manga_chapter_data: Dict[str, Dict[str, Union[str, int]]] = {
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

        def get_chapter_images(self, chapter: str, wait_time: float) -> List[str]:
            """Get chapter images as a list (full links).

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

        def create_metadata(self, chapter: str) -> Dict[str, Union[str, int, None]]:
            """Get metadata with correct keys for ComicInfo.xml.

            Provide as much metadata as possible. empty/false values will be ignored.

            Args:
                chapter: The chapter number (chapter data index)

            Returns:
                The metadata as a dict
            """
            # metadata types. have to be valid
            # {key: (type, default value, valid values)}
            {
                "Title": (str, None, []),
                "Series": (str, None, []),
                "Number": (str, None, []),
                "Count": (int, None, []),
                "Volume": (int, None, []),
                "AlternateSeries": (str, None, []),
                "AlternateNumber": (str, None, []),
                "AlternateCount": (int, None, []),
                "Summary": (str, None, []),
                "Notes": (
                    str,
                    "Downloaded with https://github.com/olofvndrhr/manga-dlp",
                    [],
                ),
                "Year": (int, None, []),
                "Month": (int, None, []),
                "Day": (int, None, []),
                "Writer": (str, None, []),
                "Colorist": (str, None, []),
                "Publisher": (str, None, []),
                "Genre": (str, None, []),
                "Web": (str, None, []),
                "PageCount": (int, None, []),
                "LanguageISO": (str, None, []),
                "Format": (str, None, []),
                "BlackAndWhite": (str, None, ["Yes", "No", "Unknown"]),
                "Manga": (str, "Yes", ["Yes", "No", "Unknown", "YesAndRightToLeft"]),
                "ScanInformation": (str, None, []),
                "SeriesGroup": (str, None, []),
                "AgeRating": (
                    str,
                    None,
                    [
                        "Unknown",
                        "Adults Only 18+",
                        "Early Childhood",
                        "Everyone",
                        "Everyone 10+",
                        "G",
                        "Kids to Adults",
                        "M",
                        "MA15+",
                        "Mature 17+",
                        "PG",
                        "R18+",
                        "Rating Pending",
                        "Teen",
                        "X18+",
                    ],
                ),
                "CommunityRating": (int, None, [1, 2, 3, 4, 5]),
            }

            # example
            return {
                "Volume": "abc",
                "LanguageISO": "en",
                "Title": "test",
            }
