import requests
import re
import mangadlp.utils as MUtils


class Mangadex():

  # api information
  api_base_url = ''
  img_base_url = ''


  # get infos to initiate class
  def __init__(self, manga_url, manga_lang):
    self.manga_url = manga_url
    self.manga_lang = manga_lang
    self.manga_title = self.get_manga_title(self.manga_uuid)
    self.manga_chapter_data = self.get_manga_chapters(self.manga_uuid)


  # get the title of the manga (and fix the filename)
  def get_manga_title(self):

    return MUtils.fix_name(title)


  # get all chapter data for further parsing
  def get_manga_chapters(self):
    chap_data_list = []

    # default mapping of chapter data
    chapter_vol = [0]
    chapter_num = [1]
    chapter_uuid = [2]
    chapter_hash = [3]
    chapter_name = [4]
    chapter_img_data = [5]

    return chap_data_list


  # get index of chapter
  def get_chapter_index(self, chapter, forcevol):

    return chapter_index


  # create list of chapters
  def create_chapter_list(self, chapter_data, forcevol):
    chapter_list = []

    return chapter_list


  # get list of image urls
  def get_img_urls(self, images):
    img_urls = []

    return img_urls


