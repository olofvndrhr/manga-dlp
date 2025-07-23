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
    assert e.type is TypeError


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
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    chapter_infos = test.manga_chapter_data["1"]
    chapter_uuid = chapter_infos["uuid"]
    chapter_name = chapter_infos["name"]
    chapter_num = chapter_infos["chapter"]
    chapter_volume = chapter_infos["volume"]

    assert [chapter_uuid, chapter_name, chapter_volume, chapter_num] == [
        "ec0f5cb6-8e87-48b8-86b3-5718bdee0f29",
        "Yona",
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
    assert e.type is KeyError


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
    assert e.type is TypeError


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
    assert e.type is KeyError


def test_not_existing_lang():
    url_uuid = (
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    )
    language = "zz"
    forcevol = False

    with pytest.raises(Exception) as e:
        Mangadex(url_uuid, language, forcevol)
    assert e.type is KeyError


def test_create_chapter_list():
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    test_list = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "5.5",
        "6",
        "6.5",
        "7",
        "8",
        "9",
        "9.5",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "15.5",
    ]

    assert test.create_chapter_list() == test_list


def test_create_chapter_list_forcevol():
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    forcevol = True
    test = Mangadex(url_uuid, language, forcevol)
    test_list = [
        "1:1",
        "1:2",
        "1:3",
        "1:4",
        "1:5",
        "1:5.5",
        "1:6",
        "1:6.5",
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

    assert test.create_chapter_list() == test_list


def test_get_chapter_images():
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    img_base_url = "https://uploads.mangadex.org"
    chapter_hash = "0c9bcd00531584a3dc14b41998991450"
    chapter_num = "1"
    test_list = [
        f"{img_base_url}/data/{chapter_hash}/1-2d60ed7ba0f529b847f40accb367478fe2173c67df21e18b1cb56d0228cdcb6d.jpg",
        f"{img_base_url}/data/{chapter_hash}/2-8a5b2e89170cf1080551a911dce9f9d9032e9d0e1f2441104d3c115bd75d35a2.jpg",
        f"{img_base_url}/data/{chapter_hash}/3-418d4b6d6afcdfa52635bf20e42fe1c5346833c8fb15b0f1f100ea3a89ff7f88.jpg",
        f"{img_base_url}/data/{chapter_hash}/4-abcd5b12ff702320fd1491710f69056f59fd33d5a65cc04b0fdce0dc9080dc0d.jpg",
        f"{img_base_url}/data/{chapter_hash}/5-5735177b237cdd61272dd1cb6f95620ac2e20804f14037dacb970cea0d4af830.jpg",
        f"{img_base_url}/data/{chapter_hash}/6-70e5fbe2b90f95e8d396c4b0bcf2965d8c6eb78b9dccefcfc1719f01e64b599b.jpg",
        f"{img_base_url}/data/{chapter_hash}/7-a16089859eb5508d5e6572cad0acaa99d64f1c8dca6d6a12708bc442115e7839.jpg",
        f"{img_base_url}/data/{chapter_hash}/8-8353d0cebefa554dcd42919f0da38da33f5fa6d41a400b522cbaddaacdbfb8ee.jpg",
        f"{img_base_url}/data/{chapter_hash}/9-3c547dc519c35bbe4e4374d326521289160d9fe1af50f24c8d4a979c390c2695.jpg",
        f"{img_base_url}/data/{chapter_hash}/10-386c8425fc688e74b2dae4bfcd51327fba7afd181d854a86731d964b1a88d4b6.jpg",
        f"{img_base_url}/data/{chapter_hash}/11-1d8e27a01ef2ee6ea48bba094d6343703f415a4846026fc019ddaf5920df7056.jpg",
        f"{img_base_url}/data/{chapter_hash}/12-845b455acced1ee3f879d92d28b0118e99b929aba93ef822cdc7236524fabe45.jpg",
        f"{img_base_url}/data/{chapter_hash}/13-0557969bfebc40f0b8bbc872db934fbd01a891a70048fb2fbbd9b58ecc02f0a5.jpg",
        f"{img_base_url}/data/{chapter_hash}/14-3b4526d60a20e32a3345b700d8093b60c6b608e751608c2f20f64be0a0a75eec.jpg",
        f"{img_base_url}/data/{chapter_hash}/15-f60d40740f544c0a84de85ce586872a450b996a37edf313c3b2512b1b810a0d6.jpg",
        f"{img_base_url}/data/{chapter_hash}/16-e10fa00d1af9040a3895d91e76028736b5fa23a533446d440fbf2c47af338b8e.jpg",
        f"{img_base_url}/data/{chapter_hash}/17-f59ee24684c4fa217f2d877b3d97bb46b79a261086fdd40ed5263e1a3fa67ff6.jpg",
        f"{img_base_url}/data/{chapter_hash}/18-9fec3d9a05ab44046fdc4c7d0876e6f508942ae63a93ff998e1582da7df41b14.jpg",
        f"{img_base_url}/data/{chapter_hash}/19-e85b2568b323f043d427ad7fe1dd8ae66a02c3ea2e1155b6c3209ff353c1af64.jpg",
        f"{img_base_url}/data/{chapter_hash}/20-2a4ade9c7dccf20819901864f6a9a2301a8ac43c81533ee6c6b01588b404e05f.jpg",
        f"{img_base_url}/data/{chapter_hash}/21-1aabb88bcd9e869e3fc14c4948c2e69392730d2f414e1dd8da1a03b7fd90bb74.jpg",
        f"{img_base_url}/data/{chapter_hash}/22-f1bb17f9489a23fe46454449d3b91c8a4166a8b2ca49f283881e035e70edd5ef.jpg",
        f"{img_base_url}/data/{chapter_hash}/23-129299c00d6d7886b13318b6bda6bbdf0ede1dc65a0b6159e574db9cd1c69135.jpg",
        f"{img_base_url}/data/{chapter_hash}/24-65bcfb17e8983369472297e3a23ea69f6892ac3d7eb9852386061594504d934f.jpg",
        f"{img_base_url}/data/{chapter_hash}/25-67b869097551e4108e9295e5092e97d1153992803910ac18a2a328436dfecf74.jpg",
        f"{img_base_url}/data/{chapter_hash}/26-a0f56d7e357f61d6f85be7ee71342de0c9bd68b5c057b4d7e0082369915bd7c6.jpg",
        f"{img_base_url}/data/{chapter_hash}/27-a21f218fe32a1070c116b0faa8235a95598943933e9e69fef8ec16a8ebe86712.jpg",
        f"{img_base_url}/data/{chapter_hash}/28-fb0f43687f1faaa0e7c58465409a706d8cf15225cc3a29ce0173a91ec5586173.jpg",
        f"{img_base_url}/data/{chapter_hash}/29-4d312b1e51094137de40de267b21fd095d4acc053d771557b47bc798c778f184.jpg",
        f"{img_base_url}/data/{chapter_hash}/30-d6b059ceafd260cd26d004202e50c0b68212fecbe20e759f0af39bf5dbc4e937.jpg",
        f"{img_base_url}/data/{chapter_hash}/31-3d6939458452127e1e48ef337ce5f331fb9486148f1813d1668903e8f9a88f9c.jpg",
        f"{img_base_url}/data/{chapter_hash}/32-c2880ebf2c841da2a6a807590f1ddbeafc954ee76271689fb64fd9590eef2296.jpg",
        f"{img_base_url}/data/{chapter_hash}/33-68aaaba49062431e48091ec9ff06a0a145b1d623592c3e576b3b2df950223129.jpg",
        f"{img_base_url}/data/{chapter_hash}/34-3c7976456b3a872cf980aec580cc60f03b8fdee16aba3a6afc9d27190144a048.jpg",
        f"{img_base_url}/data/{chapter_hash}/35-f94ebf55f2358b989364d18c6d13ae02c4818037773ee4a847376be6db8e0931.jpg",
    ]
    assert test.get_chapter_images(chapter_num, 2) == test_list


def test_get_chapter_images_error(monkeypatch: MonkeyPatch):
    fail_url = "https://api.mangadex.org/at-home/server/e86ec2c4-c5e4-4710-bfaa-999999999999"
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    chapter_num = "1"
    monkeypatch.setattr(requests, "get", fail_url)

    assert not test.get_chapter_images(chapter_num, 2)


def test_chapter_metadata():
    url_uuid = "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona"
    language = "en"
    forcevol = False
    test = Mangadex(url_uuid, language, forcevol)
    chapter_metadata = test.create_metadata("1")
    manga_name = chapter_metadata["Series"]
    chapter_name = chapter_metadata["Title"]
    chapter_num = chapter_metadata["Number"]
    chapter_volume = chapter_metadata["Volume"]
    chapter_url = chapter_metadata["Web"]

    assert (manga_name, chapter_name, chapter_volume, chapter_num, chapter_url) == (
        "Yona Yona Yona",
        "Yona",
        1,
        "1",
        "https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3",
    )
