import pytest
from pathlib import Path
import mangadlp.main as MdlpMain
import mangadlp.utils as MdlpUtils
import mangadlp.downloader as MdlpDownloader

def test_readin_list():
  list_file = Path('test.txt')
  test_list = MdlpMain.readin_list(list_file)

  assert test_list == ['https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu', 'https://mangadex.org/title/bd6d0982-0091-4945-ad70-c028ed3c0917/mushoku-tensei-isekai-ittara-honki-dasu']


def check_api():
  url = 'https://mangadex.org/title/a96676e5-8ae2-425e-b549-7f15dd34a6d8/komi-san-wa-komyushou-desu'
  test = MdlpMain.check_api(url)

  assert test == eval(mangadlp.api.mangadex.Mangadex)