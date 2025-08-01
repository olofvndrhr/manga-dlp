import shutil
from pathlib import Path

import pytest

from mangadlp import app, utils


def test_make_archive_true():
    img_path = Path("tests/test_dir")
    archive_path = Path("tests/test_dir.cbz")
    file_format = ".cbz"
    img_path.mkdir(parents=True, exist_ok=True)
    for n in range(5):
        img_name = img_path / f"page{n}"
        img_name.with_suffix(".png").touch(exist_ok=True)
    utils.make_archive(img_path, file_format)
    assert archive_path.exists()
    # cleanup
    archive_path.unlink(missing_ok=True)
    img_path.with_suffix(".zip").unlink(missing_ok=True)
    shutil.rmtree(img_path, ignore_errors=True)


def test_make_archive_false():
    archive_path = Path("tests/test_dir2.cbz")
    img_path = Path("tests/test_dir2")
    file_format = "cbz"
    with pytest.raises(Exception) as e:
        utils.make_archive(img_path, file_format)
    assert e.type is FileNotFoundError
    assert not archive_path.exists()
    # cleanup
    Path("tests/test_dir2.zip").unlink()


def test_chapter_list():
    chapters_in = "1-4,8,11,14-15,22"
    chapters_out = ["1", "2", "3", "4", "8", "11", "14", "15", "22"]
    assert utils.get_chapter_list(chapters_in, []) == chapters_out


def test_chapter_list_forcevol():
    chapters_in = "1:1-1:4,2:8,3:11,4:14-4:15,5:22"
    chapters_out = ["1:1", "1:2", "1:3", "1:4", "2:8", "3:11", "4:14", "4:15", "5:22"]
    assert utils.get_chapter_list(chapters_in, []) == chapters_out


def test_chapter_list_full():
    mdlp = app.MangaDLP(
        url_uuid="https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona",
        language="en",
        chapters="",
        list_chapters=True,
        file_format="cbz",
        forcevol=True,
        download_path="tests",
        download_wait=2,
    )
    chap_list = utils.get_chapter_list("1:1,1:2,1:4-1:7,2:", mdlp.manga_chapter_list)
    assert chap_list == [
        "1:1",
        "1:2",
        "1:4",
        "1:5",
        "1:6",
        "1:7",
        "2:8",
        "2:9",
        "2:9.5",
        "2:10",
        "2:11",
        "2:12",
        "2:13",
        "2:14",
        "2:15",
        "2:15.5",
    ]


def test_fix_name():
    filename_in1 = r"..hello?; @test1-*<\>test2.cbz.."
    filename_in2 = r"!hello: >test1-/test2<!.cbz"
    filename_in3 = r"  hello test1-test2.cbz@    "
    filename_in4 = r'hello "test1"-test2..cbz.'
    filename_in5 = r'..   hello "test1"-\/test2..cbz   .'
    # out
    filename_out = "hello test1-test2.cbz"
    assert utils.fix_name(filename_in1) == filename_out
    assert utils.fix_name(filename_in2) == filename_out
    assert utils.fix_name(filename_in3) == filename_out
    assert utils.fix_name(filename_in4) == filename_out
    assert utils.fix_name(filename_in5) == filename_out


def test_get_filename_forcevol():
    manga_name = "The test manga"
    chapter_name = "The holy test Chapter"
    chapter_vol = "2"
    chapter_num = "44"
    forcevol = True
    name_format = "{default}"
    name_format_none = ""
    filename = "Vol. 2 Ch. 44 - The holy test Chapter"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_forcevol_noname():
    manga_name = "The test manga"
    chapter_name = ""
    chapter_vol = "2"
    chapter_num = "44"
    forcevol = True
    name_format = "{default}"
    name_format_none = ""
    filename = "Vol. 2 Ch. 44"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_novol():
    manga_name = "The test manga"
    chapter_name = ""
    chapter_vol = ""
    chapter_num = "1"
    forcevol = True
    name_format = "{default}"
    name_format_none = ""
    filename = "Vol. 0 Ch. 1"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename():
    manga_name = "The test manga"
    chapter_name = "The holy test Chapter"
    chapter_vol = "2"
    chapter_num = "44"
    forcevol = False
    name_format = "{default}"
    name_format_none = ""
    filename = "Ch. 44 - The holy test Chapter"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_oneshot():
    manga_name = "The test manga"
    chapter_name = "Oneshot"
    chapter_vol = ""
    chapter_num = ""
    forcevol = False
    name_format = "{default}"
    name_format_none = ""
    filename = "Oneshot"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_noname():
    manga_name = "The test manga"
    chapter_name = ""
    chapter_vol = "1"
    chapter_num = "1"
    forcevol = False
    name_format = "{default}"
    name_format_none = ""
    filename = "Ch. 1"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_custom_format():
    manga_name = "The test manga"
    chapter_name = "Test"
    chapter_vol = "1"
    chapter_num = "1"
    forcevol = False
    name_format = "{manga_title}-{chapter_name}-{chapter_num}-{chapter_vol}"
    name_format_none = ""
    filename = "The test manga-Test-1-1"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_custom_format_err():
    manga_name = "The test manga"
    chapter_name = "Test"
    chapter_vol = "1"
    chapter_num = "1"
    forcevol = False
    name_format = "{chapter_test}-{chapter_num}-{chapter_vol}"
    name_format_none = ""
    filename = "Ch. 1 - Test"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )


def test_get_filename_custom_format_none():
    manga_name = "The test manga"
    chapter_name = ""
    chapter_vol = "1"
    chapter_num = ""
    forcevol = False
    name_format = "{chapter_name}-{chapter_num}-{chapter_vol}"
    name_format_none = "ABC"
    filename = "ABC-ABC-1"
    assert (
        utils.get_filename(
            manga_name,
            chapter_name,
            chapter_vol,
            chapter_num,
            forcevol,
            name_format,
            name_format_none,
        )
        == filename
    )
