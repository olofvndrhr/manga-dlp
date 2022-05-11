import os
import shutil
from pathlib import Path

import mangadlp.main as MdlpMain
from mangadlp.api.mangadex import Mangadex


def test_readin_list():
    list_file = Path("tests/test_list.txt")
    test_list = MdlpMain.readin_list(list_file)

    assert test_list == [
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu",
        "https://mangadex.org/title/bd6d0982-0091-4945-ad70-c028ed3c0917/mushoku-tensei-isekai-ittara-honki-dasu",
        "37f5cce0-8070-4ada-96e5-fa24b1bd4ff9",
    ]


def test_check_api():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    test = MdlpMain.check_api(url)

    assert test == Mangadex


def test_full():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    lang = "en"
    chapters = "1"
    readlist = ""
    list_chapters = False
    nocbz = False
    forcevol = False
    download_path = "tests"
    download_wait = 1
    verbose = False
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
