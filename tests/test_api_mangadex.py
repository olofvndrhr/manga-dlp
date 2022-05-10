from mangadlp.api.mangadex import Mangadex


def test_uuid_link():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    lang = "en"
    forcevol = False
    verbose = False
    test = Mangadex(url, lang, forcevol, verbose)
    assert test.manga_uuid == "a96676e5-8ae2-425e-b549-7f15dd34a6d8"


def test_uuid_pure():
    url = "a96676e5-8ae2-425e-b549-7f15dd34a6d8"
    lang = "en"
    forcevol = False
    verbose = False
    test = Mangadex(url, lang, forcevol, verbose)
    assert test.manga_uuid == "a96676e5-8ae2-425e-b549-7f15dd34a6d8"


def test_title():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    lang = "en"
    forcevol = False
    verbose = False
    test = Mangadex(url, lang, forcevol, verbose)
    assert test.manga_title == "Komi-san wa Komyushou Desu"


def test_chapter_infos():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    lang = "en"
    forcevol = False
    verbose = False
    test = Mangadex(url, lang, forcevol, verbose)
    chapter_infos = test.get_chapter_infos("1")
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
