import shutil
import subprocess
import time
from pathlib import Path

import pytest
import xmlschema

from mangadlp.metadata import validate_metadata, write_metadata


@pytest.fixture
def wait_20s():
    print("sleeping 20 seconds because of api timeouts")
    time.sleep(20)


def test_metadata_creation():
    test_metadata_file = Path("tests/ComicInfo_test.xml")
    metadata_path = Path("tests/")
    metadata_file = Path("tests/ComicInfo.xml")
    metadata = {
        "Volume": 1,
        "Number": "2",
        "PageCount": 99,
        "Count": 10,
        "LanguageISO": "en",
        "Title": "title1",
        "Series": "series1",
        "Summary": "summary1",
        "Genre": "genre1",
        "Web": "https://mangadex.org",
        "Format": "cbz",
    }

    write_metadata(metadata_path, metadata)
    assert metadata_file.exists()

    read_in_metadata = metadata_file.read_text(encoding="utf8")
    test_metadata = test_metadata_file.read_text(encoding="utf8")
    assert test_metadata == read_in_metadata

    # cleanup
    metadata_file.unlink()


def test_metadata_validation():
    metadata = {
        "Volume": "1",  # invalid
        "Number": "2",
        "PageCount": "99",  # invalid
        "Count": "10",  # invalid
        "LanguageISO": 1,  # invalid
        "Title": "title1",
        "Series": "series1",
        "Summary": "summary1",
        "Genre": "genre1",
        "Web": "https://mangadex.org",
        "Format": "cbz",
    }

    valid_metadata = validate_metadata(metadata)

    assert valid_metadata["ComicInfo"] == {
        "Title": "title1",
        "Series": "series1",
        "Number": "2",
        "Summary": "summary1",
        "Notes": "Downloaded with https://github.com/olofvndrhr/manga-dlp",
        "Genre": "genre1",
        "Web": "https://mangadex.org",
        "Format": "cbz",
        "Manga": "Yes",
    }


def test_metadata_validation_values():
    metadata = {
        "BlackAndWhite": "No",
        "Manga": "YesAndRightToLeft",
        "AgeRating": "Rating Pending",
        "CommunityRating": 4,
    }

    valid_metadata = validate_metadata(metadata)

    assert valid_metadata["ComicInfo"] == {
        "Notes": "Downloaded with https://github.com/olofvndrhr/manga-dlp",
        "BlackAndWhite": "No",
        "Manga": "YesAndRightToLeft",
        "AgeRating": "Rating Pending",
        "CommunityRating": 4,
    }


def test_metadata_validation_values2():
    metadata = {
        "BlackAndWhite": "No",
        "Manga": "YesAndRightToLeft",
        "AgeRating": "12+",  # invalid
        "CommunityRating": 10,  # invalid
    }

    valid_metadata = validate_metadata(metadata)

    assert valid_metadata["ComicInfo"] == {
        "Notes": "Downloaded with https://github.com/olofvndrhr/manga-dlp",
        "BlackAndWhite": "No",
        "Manga": "YesAndRightToLeft",
    }


def test_metadata_chapter_validity(wait_20s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    metadata_path = manga_path / "Ch. 1 - Once In A Life Time Misfire/ComicInfo.xml"
    language = "en"
    chapters = "1"
    download_path = "tests"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        download_path,
        "--format",
        "",
        "--debug",
    ]
    schema = xmlschema.XMLSchema("mangadlp/metadata/ComicInfo_v2.0.xsd")

    script_path = "manga-dlp.py"
    command = ["python3", script_path] + command_args

    assert subprocess.call(command) == 0
    assert metadata_path.is_file()
    assert schema.is_valid(metadata_path)

    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
