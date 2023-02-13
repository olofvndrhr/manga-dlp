from pathlib import Path

from mangadlp.metadata import write_metadata


def test_metadata_creation():
    test_metadata_file = Path("tests/ComicInfo_test.xml")
    metadata_path = Path("tests/")
    metadata_file = Path("tests/ComicInfo.xml")
    metadata = {
        "Volume": "1",
        "Number": "2",
        "PageCount": "99",
        "Count": "10",
        "LanguageISO": "en",
        "Title": "title1",
        "Series": "series1",
        "Summary": "summary1",
        "Genre": "genre1",
        "Web": "https://mangadex.org",
    }

    write_metadata(metadata_path, metadata)
    assert metadata_file.exists()

    read_in_metadata = metadata_file.read_text(encoding="utf8")
    test_metadata = test_metadata_file.read_text(encoding="utf8")
    assert test_metadata == read_in_metadata

    # cleanup
    metadata_file.unlink()
