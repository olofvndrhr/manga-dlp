import os
from pathlib import Path

import pytest

import mangadlp.cli as mdlpinput


def test_read_and_url():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    link_file = "tests/testfile.txt"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-u {url_uuid} --read {link_file} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_no_read_and_url():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    link_file = "tests/testfile.txt"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-l {language} -c {chapters} --path {download_path} --format {file_format} --debug"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_no_chaps():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = ""
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-u {url_uuid} -l {language} --path {download_path} --format {file_format} --debug"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_no_volume():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --debug --forcevol"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_readin_list():
    list_file = "tests/test_list.txt"
    test_list = mdlpinput.readin_list(None, None, list_file)

    assert test_list == [
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu",
        "https://mangadex.org/title/bd6d0982-0091-4945-ad70-c028ed3c0917/mushoku-tensei-isekai-ittara-honki-dasu",
        "37f5cce0-8070-4ada-96e5-fa24b1bd4ff9",
    ]
