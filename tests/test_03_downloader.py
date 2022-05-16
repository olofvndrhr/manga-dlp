from pathlib import Path
import pytest
import requests
import mangadlp.downloader as downloader
import shutil


def test_downloader():
    urls = [
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A1-c111d78b798f1dda1879334a3478f7ae4503578e8adf1af0fcc4e14d2a396ad4.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A2-717ec3c83e8e05ed7b505941431a417ebfed6a005f78b89650efd3b088b951ec.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A3-95f1b873d75f7fb820cf293df903ca37264d4af8963f44d154418c529c737547.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A4-defb89c1919b7721d3b09338f175186cabe4e292e4925818a6982581378f1966.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A5-8d852ab3e9ddb070d8ba70bc5c04d78012032975b3a69603cc88a4a8d12652d4.png",
    ]
    chapter_path = Path("tests/test_folder1")
    chapter_path.mkdir(parents=True, exist_ok=True)
    images = []
    assert downloader.download_chapter(urls, chapter_path, 0.5, True)
    for file in chapter_path.iterdir():
        images.append(file.name)

    print(images)
    assert images == ["001", "002", "003", "004", "005"]
    # cleanup
    shutil.rmtree(chapter_path, ignore_errors=True)


def test_downloader_fail(monkeypatch):
    images = [
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A1-c111d78b798f1dda1879334a3478f7ae4503578e8adf1af0fcc4e14d2a396ad4.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A2-717ec3c83e8e05ed7b505941431a417ebfed6a005f78b89650efd3b088b951ec.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A3-95f1b873d75f7fb820cf293df903ca37264d4af8963f44d154418c529c737547.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A4-defb89c1919b7721d3b09338f175186cabe4e292e4925818a6982581378f1966.png",
        "https://uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A5-8d852ab3e9ddb070d8ba70bc5c04d78012032975b3a69603cc88a4a8d12652d4.png",
    ]
    fail_url = (
        "https://_uploads.mangadex.org/data/f1117c5e7aff315bc3429a8791c89d63/A4-defb89c1919b7721d3b09338f175186cabe4e292e4925818a6982581378f1966.png",
    )
    chapter_path = Path("tests/test_folder1")
    chapter_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(requests, "get", fail_url)
    with pytest.raises(ConnectionError) as e:
        downloader.download_chapter(images, chapter_path, 0.5, True)

    assert e.type == ConnectionError
    # cleanup
    shutil.rmtree(chapter_path, ignore_errors=True)
