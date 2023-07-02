import shutil
import subprocess
import time
from pathlib import Path

import pytest
from pytest import MonkeyPatch


@pytest.fixture
def wait_10s(_: MonkeyPatch):
    print("sleeping 10 seconds because of api timeouts")
    time.sleep(10)


@pytest.fixture
def wait_20s(_: MonkeyPatch):
    print("sleeping 20 seconds because of api timeouts")
    time.sleep(20)


def test_manga_pre_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    language = "en"
    chapters = "1"
    download_path = "tests"
    manga_pre_hook = "touch tests/manga-pre.txt"
    hook_file = Path("tests/manga-pre.txt")
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        download_path,
        "--debug",
        "--hook-manga-pre",
        manga_pre_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()

    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
    hook_file.unlink()


def test_manga_post_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    language = "en"
    chapters = "1"
    download_path = "tests"
    manga_post_hook = "touch tests/manga-post.txt"
    hook_file = Path("tests/manga-post.txt")
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        download_path,
        "--debug",
        "--hook-manga-post",
        manga_post_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()

    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
    hook_file.unlink()


def test_chapter_pre_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    language = "en"
    chapters = "1"
    download_path = "tests"
    chapter_pre_hook = "touch tests/chapter-pre.txt"
    hook_file = Path("tests/chapter-pre.txt")
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        download_path,
        "--debug",
        "--hook-chapter-pre",
        chapter_pre_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()

    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
    hook_file.unlink()


def test_chapter_post_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    language = "en"
    chapters = "1"
    download_path = "tests"
    chapter_post_hook = "touch tests/chapter-post.txt"
    hook_file = Path("tests/chapter-post.txt")
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        download_path,
        "--debug",
        "--hook-chapter-post",
        chapter_post_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()

    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
    hook_file.unlink()


def test_all_hooks(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    language = "en"
    chapters = "1"
    download_path = "tests"
    manga_pre_hook = "touch tests/manga-pre2.txt"
    manga_post_hook = "touch tests/manga-post2.txt"
    chapter_pre_hook = "touch tests/chapter-pre2.txt"
    chapter_post_hook = "touch tests/chapter-post2.txt"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        download_path,
        "--debug",
        "--hook-manga-pre",
        manga_pre_hook,
        "--hook-manga-post",
        manga_post_hook,
        "--hook-chapter-pre",
        chapter_pre_hook,
        "--hook-chapter-post",
        chapter_post_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert Path("tests/manga-pre2.txt").is_file()
    assert Path("tests/manga-post2.txt").is_file()
    assert Path("tests/chapter-pre2.txt").is_file()
    assert Path("tests/chapter-post2.txt").is_file()

    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)
    Path("tests/manga-pre2.txt").unlink()
    Path("tests/manga-post2.txt").unlink()
    Path("tests/chapter-pre2.txt").unlink()
    Path("tests/chapter-post2.txt").unlink()
