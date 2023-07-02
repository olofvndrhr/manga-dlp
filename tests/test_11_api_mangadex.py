import pytest
import requests
from pytest import MonkeyPatch

from mangadlp.api.mangadex import Mangadex


def test_uuid_link():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)

    assert test.manga_uuid == "a96676e5-8ae2-425e-b549-7f15dd34a6d8"


def test_uuid_pure():
    url_uuid = "a96676e5-8ae2-425e-b549-7f15dd34a6d8"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)

    assert test.manga_uuid == "a96676e5-8ae2-425e-b549-7f15dd34a6d8"


def test_uuid_link_false():
    url_uuid = "https://mangadex.org/title/a966-76e-5-8a-e2-42-5e-b-549-7f15dd-34a6d8/komi-san-wa-komyushou-desu"
    language = "en"
    forcevol = False

    with pytest.raises(Exception) as e:
        Mangadex(url_uuid, language, forcevol)
    assert e.type == TypeError


def test_title():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)

    assert test.manga_title == "Komi-san wa Komyushou Desu"


def test_alt_title():
    url_uuid = "https://mangadex.org/title/5a90308a-8b12-4a4d-9c6d-2487028fe319/uzaki-chan-wants-to-hang-out"
    language = "fr"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)

    assert test.manga_title == "Uzaki-chan wants to hang out"


def test_alt_title_fallback():
    url_uuid = (
        "https://mangadex.org/title/d7037b2a-874a-4360-8a7b-07f2899152fd/mairimashita-iruma-kun"
    )
    language = "fr"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)

    assert test.manga_title == "Iruma à l’école des démons"  # noqa


def test_chapter_infos():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    chapter_infos = test.manga_chapter_data["1"]
    chapter_uuid = chapter_infos["uuid"]
    chapter_name = chapter_infos["name"]
    chapter_num = chapter_infos["chapter"]
    chapter_volume = chapter_infos["volume"]

    assert [chapter_uuid, chapter_name, chapter_volume, chapter_num] == [
        "e86ec2c4-c5e4-4710-bfaa-7604f00939c7",
        "A Normal Person",
        "1",
        "1",
    ]


def test_non_existing_manga():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-999999999999/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False

    with pytest.raises(Exception) as e:
        Mangadex(url_uuid, language, forcevol)
    assert e.type == KeyError


def test_api_failure(monkeypatch: MonkeyPatch):
    fail_url = "https://api.mangadex.nonexistant/manga/a96676e5-8ae2-425e-b549-7f15dd34a6d8"
    monkeypatch.setattr(requests, "get", fail_url)
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False

    with pytest.raises(Exception) as e:
        Mangadex(url_uuid, language, forcevol)
    assert e.type == TypeError


def test_chapter_lang_en():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)

    assert test.check_chapter_lang() > 0


def test_empty_chapter_lang():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "ch"
    forcevol = False

    with pytest.raises(Exception) as e:
        Mangadex(url_uuid, language, forcevol)
    assert e.type == KeyError


def test_not_existing_lang():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "zz"
    forcevol = False

    with pytest.raises(Exception) as e:
        Mangadex(url_uuid, language, forcevol)
    assert e.type == KeyError


def test_create_chapter_list():
    url_uuid = "https://mangadex.org/title/6fef1f74-a0ad-4f0d-99db-d32a7cd24098/fire-punch"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    test_list = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "34.5",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "80",
        "81",
        "82",
        "83",
    ]

    assert test.create_chapter_list() == test_list


def test_create_chapter_list_forcevol():
    url_uuid = "https://mangadex.org/title/6fef1f74-a0ad-4f0d-99db-d32a7cd24098/fire-punch"
    language = "en"
    forcevol = True
    test = Mangadex(url_uuid, language, forcevol)
    test_list = [
        "1:1",
        "1:2",
        "1:3",
        "1:4",
        "1:5",
        "1:6",
        "1:7",
        "1:8",
        "2:9",
        "2:10",
        "2:11",
        "2:12",
        "2:13",
        "2:14",
        "2:15",
        "2:16",
        "2:17",
        "2:18",
        "3:19",
        "3:20",
        "3:21",
        "3:22",
        "3:23",
        "3:24",
        "3:25",
        "3:26",
        "3:27",
        "3:28",
        "4:29",
        "4:30",
        "4:31",
        "4:32",
        "4:33",
        "4:34",
        "4:34.5",
        "4:35",
        "4:36",
        "4:37",
        "4:38",
        "4:39",
        "5:40",
        "5:41",
        "5:42",
        "5:43",
        "5:44",
        "5:45",
        "5:46",
        "5:47",
        "5:48",
        "5:49",
        "6:50",
        "6:51",
        "6:52",
        "6:53",
        "6:54",
        "6:55",
        "6:56",
        "6:57",
        "6:58",
        "6:59",
        "6:60",
        "7:61",
        "7:62",
        "7:63",
        "7:64",
        "7:65",
        "7:66",
        "7:67",
        "7:68",
        "7:69",
        "7:70",
        "8:71",
        "8:72",
        "8:73",
        "8:74",
        "8:75",
        "8:76",
        "8:77",
        "8:78",
        "8:79",
        "8:80",
        "8:81",
        "8:82",
        "8:83",
    ]

    assert test.create_chapter_list() == test_list


def test_get_chapter_images():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    img_base_url = "https://uploads.mangadex.org"
    chapter_hash = "0752bc5db298beff6b932b9151dd8437"
    chapter_num = "1"
    test_list = [
        f"{img_base_url}/data/{chapter_hash}/x1-0deb4c9bfedd5be49e0a90cfb17cf343888239898c9e7451d569c0b3ea2971f4.jpg",
        f"{img_base_url}/data/{chapter_hash}/x2-48c954f2f3a38211a7f461967cbceb068558d92b993cf535b26da36dfe356bb5.jpg",
        f"{img_base_url}/data/{chapter_hash}/x3-4578e53162520f459a8329f5440d28257be4c6fb0c2dfdba43695dbd59623c11.jpg",
        f"{img_base_url}/data/{chapter_hash}/x4-5fb8eb5e405a8d006fd1d325fe7d2396d4a65f8e1cbe8a5ca205d63f30d9897b.jpg",
        f"{img_base_url}/data/{chapter_hash}/x5-8a6abe9f5d1993b1f132f6461852d954adcc3fb214c160cda39aa8be2c080694.jpg",
        f"{img_base_url}/data/{chapter_hash}/x6-44f4bb7754798762d3960b6b21d3d2c6a28aeb589c11c1b6c9685f9e495b3446.jpg",
        f"{img_base_url}/data/{chapter_hash}/x7-11f65ce481b588e276ce391a45a26f6ccbe9fd8c9cebe6334c53d21d6cddcfa0.jpg",
        f"{img_base_url}/data/{chapter_hash}/x8-f7e369b49b577f4d27f036520c3b53041ded8009bb50d140cda8f85f549baadd.png",
        f"{img_base_url}/data/{chapter_hash}/x9-61c39d0150d3acb9b3c590b6519278aa1c64019926e10e2905f5523e4e1fffdc.png",
        f"{img_base_url}/data/{chapter_hash}/x10-0b8d9b9c623e1824c45a862a57147166ec3f638ae983c8366338e4ae5f7d862a.png",
        f"{img_base_url}/data/{chapter_hash}/x11-ab4e73dc9cd24a47cbdd1223dcf37233ec17f00f21213ac24a225f45a431c27d.png",
        f"{img_base_url}/data/{chapter_hash}/x12-b26d1f605ea402145931ed29dd60820865daab82483d6527e1aa51592eebb2b8.png",
        f"{img_base_url}/data/{chapter_hash}/x13-54d9718036b9d79e930e448b592c4a3df9045ed5b8c22ab411b09dadb864756f.jpg",
        f"{img_base_url}/data/{chapter_hash}/x14-f6ed71bbb9af2bceab51028b460813c57935c923e1872fb277beb21d54425434.jpg",
    ]
    assert test.get_chapter_images(chapter_num, 2) == test_list


def test_get_chapter_images_error(monkeypatch: MonkeyPatch):
    fail_url = "https://api.mangadex.org/at-home/server/e86ec2c4-c5e4-4710-bfaa-999999999999"
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    chapter_num = "1"
    monkeypatch.setattr(requests, "get", fail_url)

    assert not test.get_chapter_images(chapter_num, 2)


def test_chapter_metadata():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    chapter_metadata = test.create_metadata("1")
    manga_name = chapter_metadata["Series"]  # pyright:ignore
    chapter_name = chapter_metadata["Title"]  # pyright:ignore
    chapter_num = chapter_metadata["Number"]  # pyright:ignore
    chapter_volume = chapter_metadata["Volume"]  # pyright:ignore
    chapter_url = chapter_metadata["Web"]  # pyright:ignore

    assert (manga_name, chapter_name, chapter_volume, chapter_num, chapter_url) == (
        "Komi-san wa Komyushou Desu",
        "A Normal Person",
        1,
        "1",
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8",
    )
