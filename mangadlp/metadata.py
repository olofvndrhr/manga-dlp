from pathlib import Path

import xmltodict
from loguru import logger as log


def write_metadata(chapter_path: Path, metadata: dict) -> None:
    if metadata["Format"] == "pdf":
        log.warning("Can't add metadata for pdf format. Skipping")
        return

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
        if not value:
            continue
        try:
            metadata_empty["ComicInfo"][key]
        except KeyError:
            continue
        log.debug(f"Updating metadata: '{key}' = '{value}'")
        metadata_empty["ComicInfo"][key] = value

    metadata_export = xmltodict.unparse(metadata_empty, pretty=True, indent=" " * 4)
    metadata_file.touch(exist_ok=True)
    metadata_file.write_text(metadata_export, encoding="utf8")
