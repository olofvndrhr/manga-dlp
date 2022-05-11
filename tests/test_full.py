import os
import shutil
from pathlib import Path
import mangadlp.main as MdlpMain


def test_full_mangadex():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    lang = "en"
    chapters = "1"
    readlist = ""
    list_chapters = False
    nocbz = False
    forcevol = False
    download_path = "tests"
    download_wait = 1
    verbose = True
    manga_path = Path("tests/Komi-san wa Komyushou Desu")
    chapter_path = Path("tests/Komi-san wa Komyushou Desu/Ch. 1 - A Normal Person.cbz")
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
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    lang = "en"
    chapters = "1"
    download_path = "tests"
    manga_path = Path("tests/Komi-san wa Komyushou Desu")
    chapter_path = Path("tests/Komi-san wa Komyushou Desu/Ch. 1 - A Normal Person.cbz")
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
