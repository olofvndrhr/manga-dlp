from pathlib import Path
import re
from mangadlp import api
import mangadlp.utils as MUtils
import mangadlp.downloader as MDownloader
# supported api's
from mangadlp.api.mangadex import Mangadex


def main(manga_url='',
        manga_language='en',
        manga_chapters=None,
        manga_readlist='',
        manga_list_chapters=False,
        manga_nocbz=False,
        manga_forcevol=False,
        download_path='downloads',
        download_wait=0.5,
        log_verbose=False):
  '''Download Mangas from supported sites\n

  Args:\n
    url (str) -- Manga URL to Download. No defaults\n
    lang (str) -- Language to download chapters in. Defaults to "en" -> english\n
    chapter (str) -- Chapters to download "all" for every chapter available. Defaults to none\n
    readlist (str) -- List of chapters to read in. One link per line. No defaults\n
    list_chapters (bool) -- If it should only list all available chapters. Defaults to False\n
    nocbz (bool) -- If the downloaded images should not be packed into a .cbz archive. Defaults to false\n
    forcevol (bool) -- Force naming of volumes. For mangas where chapters reset each volume. Defaults to false.\n
    download_path (str) -- Folder to save mangas to. Defaults to "<script_dir>/downloads"\n
    download_wait (float) -- Time to wait for each picture to download in seconds(float). Defaults 0.5.\n
    log_verbose (bool) -- If verbose logging is enabled. Defaults to false\n

  Returns:\n
    nothing\n
  '''
  # prechecks userinput/options
  if not manga_list_chapters and manga_chapters == None:
    # no chapters to download were given
    print(f'You need to specify one or more chapters to download. To see all chapters use "--list"')
    exit(1)
  # no url and no readin list given
  elif not manga_url and not manga_readlist:
    print(f'You need to specify a manga url with "-u" or a list with "--read"')
    exit(1)
  # url and readin list given
  elif manga_url and manga_readlist:
    print(f'You can only use "-u" or "--read". Dont specify both')
    exit(1)

  # check if readin file was specified
  if manga_readlist:
    # loop trough every chapter in readin file
    for url in readin_list(manga_readlist):
      ApiUsed = check_api(url)
      if not ApiUsed:
        continue
      if log_verbose:
        print(f'Api used: {ApiUsed}')
      # get manga
      get_manga(ApiUsed, url, manga_language, manga_chapters, manga_list_chapters, manga_nocbz, manga_forcevol, download_path, download_wait, log_verbose)
  else:
    # single manga
    ApiUsed = check_api(manga_url)
    if not ApiUsed:
      exit(1)
    if log_verbose:
        print(f'Api used: {ApiUsed}')
    # get manga
    get_manga(ApiUsed, manga_url, manga_language, manga_chapters, manga_list_chapters, manga_nocbz, manga_forcevol, download_path, download_wait, log_verbose)


# read in the list of links from a file
def readin_list(manga_readlist):
  url_file = Path(manga_readlist)
  url_list = []
  with url_file.open('r') as file:
    for line in file:
      url_list.append(line.rstrip())

  return url_list


# check the api which needs to be used
def check_api(manga_url):
  # apis to check
  api_mangadex = re.compile('mangadex.org')
  api_test = re.compile('test.test')
  # check url for match
  if api_mangadex.search(manga_url):
    return Mangadex
  # this is only for testing multiple apis
  elif api_test.search(manga_url):
    pass
  # no supported api found
  else:
    print(f'No supported api in link found\n{manga_url}')
    return False


# main function to get the chapters
def get_manga(ApiUsed, manga_url, manga_language, manga_chapters, manga_list_chapters, manga_nocbz, manga_forcevol, download_path, download_wait, log_verbose):
  # init api
  Api = ApiUsed(manga_url, manga_language)
  # get manga title and uuid
  manga_uuid = Api.manga_uuid
  manga_title = Api.manga_title
  # get chapter data
  manga_chapter_data = Api.manga_chapter_data
  # crate chapter list
  manga_chapter_list = Api.create_chapter_list(manga_chapter_data, manga_forcevol)

  # print infos
  print('\n=========================================')
  print(f'Manga Name: {manga_title}')
  print(f'UUID: {manga_uuid}')
  print(f'Total chapters: {len(manga_chapter_list)}')

  # list chapters if manga_list_chapters is true
  if manga_list_chapters:
    print(f'Available Chapters:\n{", ".join(manga_chapter_list)}')
    print('=========================================\n')
    return

  # check chapters to download if it not all
  chapters_to_download = []
  if manga_chapters.lower() == 'all':
    chapters_to_download = manga_chapter_list
  else:
    chapters_to_download = MUtils.get_chapter_list(manga_chapters)

  # show chapters to download
  print(f'Chapters selected:\n{", ".join(chapters_to_download)}')
  print('=========================================\n')

  # create manga folder
  manga_path = Path(f'{download_path}/{manga_title}')
  manga_path.mkdir(parents=True, exist_ok=True)

  # main download loop
  for chapter in chapters_to_download:
    # get index of chapter
    chapter_index = Api.get_chapter_index(chapter, manga_forcevol)

    # default mapping of chapter data
    chapter_vol = chapter_index[0]
    chapter_num = chapter_index[1]
    chapter_uuid = chapter_index[2]
    chapter_hash = chapter_index[3]
    chapter_name = chapter_index[4]
    chapter_img_data = chapter_index[5]
    # create image urls from img data
    image_urls = Api.get_img_urls(chapter_img_data, chapter_hash)

    # get filename for chapter
    chapter_filename = MUtils.get_filename(chapter_name, chapter_vol, chapter_num, manga_forcevol)

    # set download path for chapter
    chapter_path = manga_path / chapter_filename

    # check if chapter already exists.
    # check for folder if option nocbz is given. if nocbz is not given, the folder will be overwritten
    if MUtils.check_existence(chapter_path, manga_nocbz) and manga_forcevol:
      print(f'- Vol {chapter_vol} Chapter {chapter_num} already exists. Skipping\n')
      continue
    elif MUtils.check_existence(chapter_path, manga_nocbz):
      print(f'- Chapter {chapter_num} already exists. Skipping\n')
      continue

    # create chapter folder (skips it if it already exists)
    chapter_path.mkdir(parents=True, exist_ok=True)

    # verbose log
    if log_verbose:
      print(f'Chapter UUID: {chapter_uuid}')
      print(f'Filename: {chapter_path}\n' if manga_nocbz else f'Filename: {chapter_path}.cbz\n')
      print(f'Image URLS: {image_urls}')
      print(f'DEBUG: Downloading Volume {chapter_vol}')

    # log
    if manga_forcevol:
      print(f'+ Downloading Volume {chapter_vol} Chapter {chapter_num}')
    else:
      print(f'+ Downloading Chapter {chapter_num}')

    # download images
    try:
      MDownloader.download_chapter(image_urls, chapter_path, download_wait, log_verbose)
    except:
      if manga_forcevol:
        print(f'Cant download volume {chapter_vol} chapter {chapter_num}. Exiting')
      else:
        print(f'Cant download chapter {chapter_num}. Exiting')
      exit(1)
    else:
      # Done with chapter
      if manga_forcevol:
        print(f'Successfully downloaded volume {chapter_vol} chapter {chapter_num}')
      else:
        print(f'Successfully downloaded chapter {chapter_num}')

    # make cbz of folder
    if not manga_nocbz:
      print('\n+ Creating .cbz archive')
      try:
        MUtils.make_archive(chapter_path)
      except:
        print('Could not make cbz archive')
        exit(1)

    # done with chapter
    print('Done with chapter')
    print('------------------------------\n')

  # done with manga
  print('=============================')
  print(f'Done with manga: {manga_title}')
  print('=============================\n')

