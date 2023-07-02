import os
import shutil
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


def test_full_with_all_flags(wait_20s: MonkeyPatch):
    manga_path = Path("tests/Tomo-chan wa Onna no ko")
    chapter_path = manga_path / "Ch. 1 - Once In A Life Time Misfire.cbz"
    cache_path = Path("tests/test_cache.json")
    flags = [
        "-u https://mangadex.org/title/76ee7069-23b4-493c-bc44-34ccbf3051a8/tomo-chan-wa-onna-no-ko",
        "--loglevel 10",
        "-l en",
        "-c 1",
        "--path tests",
        "--format cbz",
        "--name-format 'Ch. {chapter_num} - {chapter_name}'",
        "--name-format-none 0",
        # "--forcevol",
        "--wait 2",
        "--hook-manga-pre 'echo 0'",
        "--hook-manga-post 'echo 1'",
        "--hook-chapter-pre 'echo 2'",
        "--hook-chapter-post 'echo 3'",
        "--cache-path tests/test_cache.json",
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
