import pytest

import mangadlp.app as app
from mangadlp.api.mangadex import Mangadex


def test_check_api_mangadex():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    test = app.MangaDLP(url_uuid=url, list_chapters=True, download_wait=2)

    assert test.api_used == Mangadex


def test_check_api_none():
    url = "https://abc.defghjk/title/abc/def"
    with pytest.raises(ValueError) as e:
        app.MangaDLP(url_uuid=url, list_chapters=True, download_wait=2)
    assert e.type == ValueError
