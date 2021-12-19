import pytest
import mangadexdlp.api as MdApi
import mangadexdlp.utils as MdUtils

def test_get_uuid():
  url = 'https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu'

  assert MdApi.get_manga_uuid(url) == 'a96676e5-8ae2-425e-b549-7f15dd34a6d8'

def test_get_chapter_list():
  chapters = '1,2,4-6'

  assert MdUtils.get_chapter_list(chapters) == ['1', '2', '4', '5', '6']
