import os
import shutil
from pathlib import Path

import mangadlp.app as app


def test_full_mangadex():
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    app.main(
        url_uuid="https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie",
        language="en",
        chapters="1",
        readlist="",
        list_chapters=False,
        file_format="cbz",
        forcevol=False,
        download_path="tests",
        download_wait=0.5,
        verbose=True,
    )

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path}"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_without_input():
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path}") != 0


def test_full_show_version():
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} --version") == 0
