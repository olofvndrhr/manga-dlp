from pathlib import Path
import shutil


def make_archive(chapter_path, manga_path):
  dst_zip = shutil.make_archive(chapter_path, 'zip', manga_path)
  dst_zip.rename(dst_zip.with_suffix('.cbz'))

def get_img_urls(manga_chapter_data):
  dl_base_url = 'https://uploads.mangadex.org'
  img_urls = []
  img_files = manga_chapter_data[4]
  chapter_hash = manga_chapter_data[2]
  for img in img_files:
    img_urls.append(f'{dl_base_url}/data/{chapter_hash}/{img}')

  return img_urls


def get_chapter_list(chapters):
  pass


