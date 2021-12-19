import pdb
import argparse
from time import sleep
import requests
import shutil
from pathlib import Path
import mangadexdlp.api as MdApi
import mangadexdlp.utils as MdUtils
import mangadexdlp.downloader as MdDownloader
import mangadexdlp.sqlite as MdSqlite



def mangadex_dlp(md_url='',md_chapters=None,md_dest='downloads',md_lang='en',md_list_chapters=False,md_nocbz=False):
  '''Download Mangas from Mangadex.org\n

  Args:\n
    url (str) -- Manga URL to Download. No defaults\n
    chapter (str/int) -- Chapters to download "all" for every chapter available. Defaults to none\n
    dest (str) -- Folder to save mangas to. Defaults to "downloads"\n
    lang (str) -- Language to download chapters in. Defaults to "en" -> english\n
    list (bool) -- If it should only list all available chapters. Defaults to False\n
    nocbz (bool) -- If the downloaded images should not be packed into a .cbz archive. Defaults to false\n

  Returns:\n
    nothing\n
  '''
  # check if md_list_chapters is true, if not check if chapters to download were specified
  if not md_list_chapters:
    if md_chapters == None:
      # no chapters to download were given
      print(f'You need to specify one or more chapters to download. To see all chapters use "--list"')
      exit(1)

  # get uuid and manga name of url
  manga_uuid = MdApi.get_manga_uuid(md_url)
  manga_title = MdApi.get_manga_title(manga_uuid, md_lang)

  print(f'Manga Name: {manga_title}')
  print(f'UUID: {manga_uuid}')

  # get chapters
  manga_chapter_data = MdApi.get_manga_chapters(manga_uuid, md_lang)
  # [0][0] = Chapter number/oneshot
  # [0][1] = Chapter UUID
  # [0][2] = Chapter Hash
  # [0][3] = Chapter Name
  # [0][4] = Chapter Data

  # crate chapter list
  manga_chapter_list = []
  for chap in manga_chapter_data:
    chapter_number = chap[0]
    manga_chapter_list.append(chapter_number)

  # list chapters if md_list_chapters is true
  if md_list_chapters:
    print(f'Available Chapters:\n{manga_chapter_list}')

  # check chapters to download if it not all
  chapters_to_download = []
  if md_chapters.lower() == 'all':
    chapters_to_download = manga_chapter_list
  else:
    chapters_to_download = MdUtils.get_chapter_list(md_chapters)

  # create manga folder
  manga_path = Path(f'{md_dest}/{manga_title}')
  manga_path.mkdir(parents=True, exist_ok=True)

  # main download loop
  for chapter in chapters_to_download:
    # get list of image urls
    list_index = manga_chapter_data.index(chapter)
    image_urls = MdUtils.get_img_urls(manga_chapter_data[list_index])
    chapter_num = manga_chapter_data[list_index][0]
    chapter_name = manga_chapter_data[list_index][3]

    # filename for chapter
    if chapter_name == None and chapter_num == 'Oneshot':
      chapter_filename = 'Oneshot'
    elif chapter_name == None:
      chapter_filename = f'Ch. {chapter_num}'
    else:
      chapter_filename = f'Ch. {chapter_num} - {chapter_name}'

    # create chapter folder
    chapter_path = manga_path / chapter_filename
    chapter_path.mkdir(parents=True, exist_ok=True)

    # download images
    print(f'Downloading Chapter {chapter_num}')
    print(f'DEBUG: Downloading Chapter {chapter}')
    try:
      MdDownloader.download_chapter(image_urls, chapter_path)
    except:
      print('Cant download chapter. Exiting')
      exit(1)
    else:
      # Done with chapter
      print(f'--Done with Chapter {chapter_num}')

    # make cbz of folder
    if not md_nocbz:
      print('Creating .cbz archive')
      try:
        MdUtils.make_archive(chapter_path, manga_path)
      except:
        print('Could not make cbz archive')
        exit(1)
      else:
        print('Done')


