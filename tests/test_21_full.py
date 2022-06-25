import os
import platform
import shutil
from pathlib import Path

import mangadlp.app as app


def test_full_api_mangadex():
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    mdlp = app.MangaDLP(
        url_uuid="https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie",
        language="en",
        chapters="1",
        list_chapters=False,
        file_format="cbz",
        forcevol=False,
        download_path="tests",
        download_wait=2,
        verbose=True,
    )
    mdlp.get_manga()

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_cbz():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_pdf():
    # check if its arm64, if yes skip this step
    if platform.machine() != "x86_64":
        return True

    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = "pdf"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.pdf")
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_folder():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = ""
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1")
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format '{file_format}' --verbose --wait 2"
    script_path = "manga-dlp.py"
    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_dir()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_skip_cbz():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose --wait 2"
    script_path = "manga-dlp.py"
    manga_path.mkdir(parents=True, exist_ok=True)
    chapter_path.touch()

    os.system(f"python3 {script_path} {command_args}")
    assert chapter_path.is_file()
    assert chapter_path.stat().st_size == 0
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_input_skip_folder():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = ""
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1")
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format '{file_format}' --verbose --wait 2"
    script_path = "manga-dlp.py"
    chapter_path.mkdir(parents=True, exist_ok=True)

    os.system(f"python3 {script_path} {command_args}")
    found_files = []
    for file in chapter_path.iterdir():
        found_files.append(file.name)

    assert chapter_path.is_dir()
    assert found_files == []
    assert not Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz").exists()
    assert not Path("tests/Shikimori's Not Just a Cutie/Ch. 1.zip").exists()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_read_cbz():
    url_list = Path("tests/test_list2.txt")
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    command_args = f"--read {str(url_list)} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose --wait 2"
    script_path = "manga-dlp.py"
    url_list.write_text(
        "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    )

    os.system(f"python3 {script_path} {command_args}")

    assert manga_path.exists() and manga_path.is_dir()
    assert chapter_path.exists() and chapter_path.is_file()
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


def test_full_with_read_skip_cbz():
    url_list = Path("tests/test_list2.txt")
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    manga_path = Path("tests/Shikimori's Not Just a Cutie")
    chapter_path = Path("tests/Shikimori's Not Just a Cutie/Ch. 1.cbz")
    command_args = f"--read {str(url_list)} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose --wait 2"
    script_path = "manga-dlp.py"
    manga_path.mkdir(parents=True, exist_ok=True)
    chapter_path.touch()
    url_list.write_text(
        "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    )

    os.system(f"python3 {script_path} {command_args}")
    assert chapter_path.is_file()
    assert chapter_path.stat().st_size == 0
    # cleanup
    shutil.rmtree(manga_path, ignore_errors=True)


# def test_full_without_input():
#     script_path = "manga-dlp.py"
#     assert os.system(f"python3 {script_path}") != 0


def test_full_show_version():
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} --version") == 0
