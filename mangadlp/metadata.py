from pathlib import Path

import xmltodict
from loguru import logger as log


def write_metadata(chapter_path: Path, metadata: dict) -> None:
    if metadata["Format"] == "pdf":
        log.warning("Can't add metadata for pdf format. Skipping")
        return

    # define metadata types
    metadata_types: dict[str, type] = {
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

    try:
        metadata_template = Path("mangadlp/metadata/ComicInfo.xml").read_text(
            encoding="utf8"
        )
        metadata_empty: dict[str, dict] = xmltodict.parse(metadata_template)
    except Exception as exc:
        log.error("Can't open or parse xml template")
        raise exc
    metadata_file = chapter_path / "ComicInfo.xml"

    log.info(f"Writing metadata to: '{metadata_file}'")
    log.debug(f"Metadata items: {metadata}")
    for key, value in metadata.items():
        # check if metadata is empty
        if not value:
            continue
        # try to match with template
        try:
            metadata_empty["ComicInfo"][key]
        except KeyError:
            continue
        # check if metadata type is correct
        log.debug(f"Key:{key} -> value={type(value)} -> check={metadata_types[key]}")
        if not isinstance(value, metadata_types[key]):  # noqa
            log.warning(
                f"Metadata has wrong type: {key}:{metadata_types[key]} -> {value}"
            )
            continue

        log.debug(f"Updating metadata: '{key}' = '{value}'")
        metadata_empty["ComicInfo"][key] = value

    metadata_export = xmltodict.unparse(metadata_empty, pretty=True, indent=" " * 4)
    metadata_file.touch(exist_ok=True)
    metadata_file.write_text(metadata_export, encoding="utf8")
