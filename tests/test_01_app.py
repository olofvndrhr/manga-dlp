from pathlib import Path

import mangadlp.app as app
from mangadlp.api.mangadex import Mangadex


def test_readin_list():
    list_file = "tests/test_list.txt"
    test = app.MangaDLP(readlist=list_file, list_chapters=True)
    test.__main__()
    test_list = test.url_list

    assert test_list == [
        "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu",
        "https://mangadex.org/title/bd6d0982-0091-4945-ad70-c028ed3c0917/mushoku-tensei-isekai-ittara-honki-dasu",
        "37f5cce0-8070-4ada-96e5-fa24b1bd4ff9",
    ]


def test_check_api():
    url = "https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu"
    test = app.MangaDLP(url_uuid=url, list_chapters=True)
    test.__main__()

    assert test.api_used == Mangadex
