from typing import List, Optional, TypedDict


class ComicInfo(TypedDict, total=False):
    """ComicInfo.xml basic types.

    Validation is done via metadata.validate_metadata()
    All valid types and values are specified in metadata.METADATA_TYPES
    """

    Title: Optional[str]
    Series: Optional[str]
    Number: Optional[str]
    Count: Optional[int]
    Volume: Optional[int]
    AlternateSeries: Optional[str]
    AlternateNumber: Optional[str]
    AlternateCount: Optional[int]
    Summary: Optional[str]
    Notes: Optional[str]
    Year: Optional[int]
    Month: Optional[int]
    Day: Optional[int]
    Writer: Optional[str]
    Colorist: Optional[str]
    Publisher: Optional[str]
    Genre: Optional[str]
    Web: Optional[str]
    PageCount: Optional[int]
    LanguageISO: Optional[str]
    Format: Optional[str]
    BlackAndWhite: Optional[str]
    Manga: Optional[str]
    ScanInformation: Optional[str]
    SeriesGroup: Optional[str]
    AgeRating: Optional[str]
    CommunityRating: Optional[int]


class ChapterData(TypedDict):
    """Basic chapter-data types.

    All values have to be provided.
    """

    uuid: str
    volume: str
    chapter: str
    name: str
    pages: int


class CacheKeyData(TypedDict):
    chapters: List[str]
    name: str


class CacheData(TypedDict):
    __root__: CacheKeyData
