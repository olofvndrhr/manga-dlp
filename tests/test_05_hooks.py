import shutil
import subprocess
import time
from pathlib import Path

import pytest
from pytest import MonkeyPatch


TESTDIR = Path("tests/testdir")
HOOKDIR = TESTDIR / "hooks"


@pytest.fixture
def wait_10s():
    print("sleeping 10 seconds because of api timeouts")
    time.sleep(10)


@pytest.fixture
def wait_20s():
    print("sleeping 20 seconds because of api timeouts")
    time.sleep(20)


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # run before each test in file
    TESTDIR.mkdir(parents=True, exist_ok=True)
    HOOKDIR.mkdir(parents=True, exist_ok=True)
    yield
    # run after each test in file
    shutil.rmtree(TESTDIR, ignore_errors=True)


def test_manga_pre_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    chapters = "1"
    hook_file = HOOKDIR / "manga-pre.txt"
    manga_pre_hook = f"touch {hook_file}"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        str(TESTDIR),
        "--debug",
        "--hook-manga-pre",
        manga_pre_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()


def test_manga_post_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    chapters = "1"
    hook_file = HOOKDIR / "manga-post.txt"
    manga_post_hook = f"touch {hook_file}"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        str(TESTDIR),
        "--debug",
        "--hook-manga-post",
        manga_post_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()


def test_chapter_pre_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    chapters = "1"
    hook_file = HOOKDIR / "chapter-pre.txt"
    chapter_pre_hook = f"touch {hook_file}"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        str(TESTDIR),
        "--debug",
        "--hook-chapter-pre",
        chapter_pre_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()


def test_chapter_post_hook(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    chapters = "1"
    hook_file = HOOKDIR / "chapter-post.txt"
    chapter_post_hook = f"touch {hook_file}"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        str(TESTDIR),
        "--debug",
        "--hook-chapter-post",
        chapter_post_hook,
    ]
    script_path = "manga-dlp.py"
    command = ["python3", script_path, *command_args]

    assert subprocess.call(command) == 0
    assert hook_file.is_file()


def test_all_hooks(wait_10s: MonkeyPatch):
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    chapters = "1"
    manga_pre_hook = f"touch {HOOKDIR}/manga-pre2.txt"
    manga_post_hook = f"touch {HOOKDIR}/manga-post2.txt"
    chapter_pre_hook = f"touch {HOOKDIR}/chapter-pre2.txt"
    chapter_post_hook = f"touch {HOOKDIR}/chapter-post2.txt"
    command_args = [
        "-u",
        url_uuid,
        "-l",
        language,
        "-c",
        chapters,
        "--path",
        str(TESTDIR),
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
    assert (HOOKDIR / "manga-pre2.txt").is_file()
    assert (HOOKDIR / "manga-post2.txt").is_file()
    assert (HOOKDIR / "chapter-pre2.txt").is_file()
    assert (HOOKDIR / "chapter-post2.txt").is_file()
