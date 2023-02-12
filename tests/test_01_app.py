import pytest

from mangadlp.api.mangadex import Mangadex
from mangadlp.app import MangaDLP


def test_check_api_mangadex():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    test = MangaDLP(url_uuid=url, list_chapters=True, download_wait=2)

    assert test.api_used == Mangadex


def test_check_api_none():
    url = "https://abc.defghjk/title/abc/def"
    with pytest.raises(ValueError) as e:
        MangaDLP(url_uuid=url, list_chapters=True, download_wait=2)
    assert e.type == ValueError
