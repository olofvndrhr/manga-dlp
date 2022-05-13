import os
import shutil
from pathlib import Path
import mangadlp.main as MdlpMain


def test_full_mangadex():
    url = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    lang = "en"
    chapters = "1"
    readlist = ""
    list_chapters = False
    nocbz = False
    forcevol = False
    download_path = "tests"
    download_wait = 0.5
    verbose = True
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    MdlpMain.main(
        url,
        lang,
        chapters,
        readlist,
        list_chapters,
        nocbz,
        forcevol,
        download_path,
        download_wait,
        verbose,
    )

    assert manga_path.exists()
    assert chapter_path.exists()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input():
    url = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    lang = "en"
    chapters = "1"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    command_args = f"-u {url} -l {lang} -c {chapters} --path {download_path}"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists()
    assert chapter_path.exists()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_without_input():
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path}") != 0
