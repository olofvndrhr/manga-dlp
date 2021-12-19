from pathlib import Path
import shutil
from zipfile import ZipFile


def make_archive(chapter_path):
  image_folder = Path(chapter_path)
  zip_path = Path(f'{chapter_path}.zip')
  with ZipFile(f'{image_folder}.zip', 'w') as zip_archive:
    for file in image_folder.iterdir():
      zip_archive.write(file, file.name)

  zip_path.rename(zip_path.with_suffix('.cbz'))
  shutil.rmtree(image_folder)


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


