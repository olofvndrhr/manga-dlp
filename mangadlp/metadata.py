from pathlib import Path
from typing import Any, Dict, Optional, Tuple, TypedDict, Union

import xmltodict
from loguru import logger as log

METADATA_FILENAME = "ComicInfo.xml"
METADATA_TEMPLATE = Path("mangadlp/metadata/ComicInfo_v2.0.xml")
# define metadata types, defaults and valid values. an empty list means no value check
# {key: (type, default value, valid values)}
METADATA_TYPES: Dict[str, Tuple[type, Any, list[Union[str, int]]]] = {
    "Title": (str, None, []),
    "Series": (str, None, []),
    "Number": (str, None, []),
    "Count": (int, None, []),
    "Volume": (int, None, []),
    "AlternateSeries": (str, None, []),
    "AlternateNumber": (str, None, []),
    "AlternateCount": (int, None, []),
    "Summary": (str, None, []),
    "Notes": (str, "Downloaded with https://github.com/olofvndrhr/manga-dlp", []),
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


def validate_metadata(metadata_in: ComicInfo) -> Dict[str, ComicInfo]:
    log.info("Validating metadata")

    metadata_valid: dict[str, ComicInfo] = {"ComicInfo": {}}
    for key, value in METADATA_TYPES.items():
        metadata_type, metadata_default, metadata_validation = value

        # add default value if present
        if metadata_default:
            log.debug(
                f"Setting default value for Key:{key} -> value={metadata_default}"
            )
            metadata_valid["ComicInfo"][key] = metadata_default

        # check if metadata key is available
        try:
            md_to_check: Union[str, int, None] = metadata_in[key]
        except KeyError:
            continue
        # check if provided metadata item is empty
        if not md_to_check:
            continue

        # check if metadata type is correct
        log.debug(f"Key:{key} -> value={type(md_to_check)} -> check={metadata_type}")
        if not isinstance(md_to_check, metadata_type):
            log.warning(
                f"Metadata has wrong type: {key}:{metadata_type} -> {md_to_check}"
            )
            continue

        # check if metadata is valid
        log.debug(f"Key:{key} -> value={md_to_check} -> valid={metadata_validation}")
        if (len(metadata_validation) > 0) and (md_to_check not in metadata_validation):
            log.warning(
                f"Metadata is invalid: {key}:{metadata_validation} -> {md_to_check}"
            )
            continue

        log.debug(f"Updating metadata: '{key}' = '{md_to_check}'")
        metadata_valid["ComicInfo"][key] = md_to_check

    return metadata_valid


def write_metadata(chapter_path: Path, metadata: ComicInfo) -> None:
    if metadata["Format"] == "pdf":  # pyright:ignore
        log.warning("Can't add metadata for pdf format. Skipping")
        return

    metadata_file = chapter_path / METADATA_FILENAME

    log.debug(f"Metadata items: {metadata}")
    metadata_valid = validate_metadata(metadata)

    log.info(f"Writing metadata to: '{metadata_file}'")
    metadata_export = xmltodict.unparse(
        metadata_valid, pretty=True, indent=" " * 4, short_empty_elements=True
    )
    metadata_file.touch(exist_ok=True)
    metadata_file.write_text(metadata_export, encoding="utf8")
