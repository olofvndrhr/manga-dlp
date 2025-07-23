from typing import TypedDict


class ComicInfo(TypedDict, total=False):
    """ComicInfo.xml basic types.

    Validation is done via metadata.validate_metadata()
    All valid types and values are specified in metadata.METADATA_TYPES
    """

    Title: str | None
    Series: str | None
    Number: str | None
    Count: int | None
    Volume: int | None
    AlternateSeries: str | None
    AlternateNumber: str | None
    AlternateCount: int | None
    Summary: str | None
    Notes: str | None
    Year: int | None
    Month: int | None
    Day: int | None
    Writer: str | None
    Colorist: str | None
    Publisher: str | None
    Genre: str | None
    Web: str | None
    PageCount: int | None
    LanguageISO: str | None
    Format: str | None
    BlackAndWhite: str | None
    Manga: str | None
    ScanInformation: str | None
    SeriesGroup: str | None
    AgeRating: str | None
    CommunityRating: int | None


class ChapterData(TypedDict):
    """Basic chapter-data types.

    All values have to be provided.
    """

    uuid: str
    volume: str
    chapter: str
    name: str
    pages: int


class CacheKeyData(TypedDict):  # noqa
    chapters: list[str]
    name: str


class CacheData(TypedDict):  # noqa
    __root__: CacheKeyData
