from pathlib import Path
import pytest
import requests
import mangadlp.input as input
import os


def test_read_and_url():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    link_file = "tests/testfile.txt"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-u {url_uuid} --read {link_file} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_no_read_and_url():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    link_file = "tests/testfile.txt"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-l {language} -c {chapters} --path {download_path} --format {file_format} --verbose"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_no_chaps():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = ""
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-u {url_uuid} -l {language} --path {download_path} --format {file_format} --verbose"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0


def test_no_volume():
    url_uuid = "https://mangadex.org/title/0aea9f43-d4a9-4bf7-bebc-550a512f9b95/shikimori-s-not-just-a-cutie"
    language = "en"
    chapters = "1"
    file_format = "cbz"
    download_path = "tests"
    command_args = f"-u {url_uuid} -l {language} -c {chapters} --path {download_path} --format {file_format} --verbose --forcevol"
    script_path = "manga-dlp.py"
    assert os.system(f"python3 {script_path} {command_args}") != 0
