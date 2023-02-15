import os
import platform
import shutil
import time
from pathlib import Path

import pytest

from mangadlp import app


@pytest.fixture
def wait_10s():
    print("sleeping 10 seconds because of api timeouts")
    time.sleep(10)


@pytest.fixture
def wait_20s():
    print("sleeping 20 seconds because of api timeouts")
    time.sleep(20)


def test_full_api_mangadex(wait_20s):
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    mdlp = app.MangaDLP(
        url_uuid="https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko",
        language="en",
        chapters="1",
        list_chapters=False,
        file_format="cbz",
        forcevol=False,
        download_path="tests",
        download_wait=2,
    )
    mdlp.get_manga()

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_cbz(wait_20s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_cbz_info(wait_20s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


@pytest.mark.skipif(
    platform.machine() != "x86_64", reason="pdf only supported on amd64"
)
def test_full_with_input_pdf(wait_20s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    language = "en"
    chapters = "1"
    file_format = "pdf"
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.pdf"
    )
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_folder(wait_20s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    language = "en"
    chapters = "1"
    file_format = ""
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire"
    )
    metadata_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire/ComicInfo.xml"
    )
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format '{file_format}' --debug --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_dir()
    assert metadata_path.exists() and metadata_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_skip_cbz(wait_10s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug --wait 2"
    script_path = "manga-dlp.py"
    manga_path.mkdir(parents=True, exist_ok=True)
    chapter_path.touch()

    os.system(f"python3 {script_path} {command_args}")
    assert chapter_path.is_file()
    assert chapter_path.stat().st_size == 0
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_skip_folder(wait_10s):
    url_uuid = "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    language = "en"
    chapters = "1"
    file_format = ""
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire"
    )
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format '{file_format}' --debug --wait 2"
    script_path = "manga-dlp.py"
    chapter_path.mkdir(parents=True, exist_ok=True)

    os.system(f"python3 {script_path} {command_args}")
    found_files = []
    for file in chapter_path.iterdir():
        found_files.append(file.name)

    assert chapter_path.is_dir()
    assert found_files == []
    assert not Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    ).exists()
    assert not Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.zip"
    ).exists()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_read_cbz(wait_20s):
    url_list = Path("tests/test_list2.txt")
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    command_args = f"--read {str(url_list)} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug --wait 2"
    script_path = "manga-dlp.py"
    url_list.write_text(
        "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    )

    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_read_skip_cbz(wait_10s):
    url_list = Path("tests/test_list2.txt")
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    command_args = f"--read {str(url_list)} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug --wait 2"
    script_path = "manga-dlp.py"
    manga_path.mkdir(parents=True, exist_ok=True)
    chapter_path.touch()
    url_list.write_text(
        "https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko"
    )

    os.system(f"python3 {script_path} {command_args}")
    assert chapter_path.is_file()
    assert chapter_path.stat().st_size == 0
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_all_flags(wait_20s):
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = Path(
        "tests/Tomo-chan wa Onna no ko/Ch. 1 - Once In A Life Time Misfire.cbz"
    )
    cache_path = Path("tests/cache.json")
    flags = [
        "-u https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko",
        "--loglevel 10",
        "-l en",
        "-c 1",
        "--path tests",
        "--format cbz",
        "--name-format 'Ch.{chapter_num} - {chapter_name}'",
        "--name-format-none 0",
        "--forcevol",
        "--wait 2",
        "--hook-manga-pre echo 0",
        "--hook-manga-post 1",
        "--hook-chapter-pre 2",
        "--hook-chapter-post 3",
        "--cache-path tests/cache.json",
        "--add-metadata",
    ]
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {' '.join(flags)}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    assert cache_path.exists() and cache_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
    cache_path.unlink(missing_ok=True)


# def test_full_without_input():
#     script_path = "manga-dlp.py"
#     assert os.system(f"python3 {script_path}") != 0


def test_full_show_version():
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} --version") == 0
