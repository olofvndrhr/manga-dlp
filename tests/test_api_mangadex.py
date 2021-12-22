import pytest
from mangadlp.api.mangadex import Mangadex

def test_uuid():
  url = 'https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu'
  lang = 'en'
  test = Mangadex(url, lang)
  assert test.get_manga_uuid() == 'a96676e5-8ae2-425e-b549-7f15dd34a6d8'


def test_title():
  url = 'https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu'
  lang = 'en'
  test = Mangadex(url, lang)
  title = test.get_manga_title(test.get_manga_uuid())
  assert title == 'Komi-san wa Komyushou Desu'


