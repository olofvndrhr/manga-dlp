import shutil
from pathlib import Path

import pytest

import mangadlp.utils as utils


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
    with pytest.raises(IOError) as e:
        utils.make_archive(img_path, file_format)
    assert e.type == IOError
    assert not archive_path.exists()
    # cleanup
    Path("tests/test_dir2.zip").unlink()


def test_chapter_list():
    chapters_in = "1-4,8,11,14-15,22"
    chapters_out = ["1", "2", "3", "4", "8", "11", "14", "15", "22"]
    assert utils.get_chapter_list(chapters_in) == chapters_out


def test_chapter_list_forcevol():
    chapters_in = "1:1-1:4,2:8,3:11,4:14-4:15,5:22"
    chapters_out = ["1:1", "1:2", "1:3", "1:4", "2:8", "3:11", "4:14", "4:15", "5:22"]
    assert utils.get_chapter_list(chapters_in) == chapters_out


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
    chapter_name = "The holy test Chapter"
    chapter_vol = "2"
    chapter_num = "44"
    forcevol = True
    filename = "Vol. 2 Ch. 44 - The holy test Chapter"
    assert (
        utils.get_filename(chapter_name, chapter_vol, chapter_num, forcevol) == filename
    )


def test_get_filename_forcevol_noname():
    chapter_name = ""
    chapter_vol = "2"
    chapter_num = "44"
    forcevol = True
    filename = "Vol. 2 Ch. 44"
    assert (
        utils.get_filename(chapter_name, chapter_vol, chapter_num, forcevol) == filename
    )


def test_get_filename():
    chapter_name = "The holy test Chapter"
    chapter_vol = "2"
    chapter_num = "44"
    forcevol = False
    filename = "Ch. 44 - The holy test Chapter"
    assert (
        utils.get_filename(chapter_name, chapter_vol, chapter_num, forcevol) == filename
    )


def test_get_filename_oneshot():
    chapter_name = "Oneshot"
    chapter_vol = ""
    chapter_num = ""
    forcevol = False
    filename = "Oneshot"
    assert (
        utils.get_filename(chapter_name, chapter_vol, chapter_num, forcevol) == filename
    )


def test_get_filename_noname():
    chapter_name = ""
    chapter_vol = "1"
    chapter_num = "1"
    forcevol = False
    filename = "Ch. 1"
    assert (
        utils.get_filename(chapter_name, chapter_vol, chapter_num, forcevol) == filename
    )
