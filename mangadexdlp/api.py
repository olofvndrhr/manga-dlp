import pdb
import requests
import re
import json
import html

api_url = 'https://api.mangadex.org'

def get_manga_uuid(manga_url):

  # isolate id from url
  md_id_regex = re.compile('[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}')
  # check for new mangadex id
  if md_id_regex.search(manga_url):
    uuid = md_id_regex.search(manga_url)[0]
  else:
    print('No valid id found')
    exit(1)

  # check if the manga exists
  try:
    req = requests.get(f'{api_url}/manga/{uuid}')
  except:
    print('Error. Maybe the MangaDex API is down?')
    exit(1)
  else:
    # check mangadex status
    response = req.json()['result']
    if response == 'ok':
      return uuid
    else:
      print('Manga not found')
      exit(1)



def get_manga_title(uuid, lang):

  req = requests.get(f'{api_url}/manga/{uuid}')
  api_resp = req.json()

  try:
    title = api_resp['data']['attributes']['title'][lang]
  except:
    # search in alt titles
    try:
      alt_titles = {}
      for val in api_resp['data']['attributes']['altTitles']:
        alt_titles.update(val)
      title = alt_titles[lang]
    except: # no title on requested language found
      print('Chapter in requested language not found.')
      exit(1)

  return title



def get_manga_chapters(uuid, lang):
  content_ratings = 'contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic'
  chap_data_list = []

  req = requests.get(f'{api_url}/manga/{uuid}/feed?limit=0&translatedLanguage[]={lang}&{content_ratings}')
  try:
    total = req.json()['total']
    print(total)
  except:
    print('Error retrieving the chapters list. Did you specify a valid language code?')
    exit(1)

  if total == 0:
    print('No chapters available to download!')
    exit(0)

  offset = 0
  while offset < total: # if more than 500 chapters!
    req = requests.get(f'{api_url}/manga/{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}&{content_ratings}')
    for chapter in req.json()['data']:
      chap_num = chapter['attributes']['chapter']
      chap_uuid = chapter['id']
      chap_hash = chapter['attributes']['hash']
      chap_data = chapter['attributes']['data']
      # chapter name, change illegal file names
      chap_name = chapter['attributes']['title']
      if not chap_name == None:
        chap_name = re.sub('[/<>:"/\\|?*!.]', '', chap_name)
      # check if the chapter is external (cant download them)
      chap_external = chapter['attributes']['externalUrl']
      # name chapter "oneshot" if there is no chapter number
      if chap_external == None and chap_num == None:
        chap_data_list.append(['Oneshot', chap_uuid, chap_hash, chap_name, chap_data])
      # else add chapter number
      elif chap_external == None:
        chap_data_list.append([chap_num, chap_uuid, chap_hash, chap_name, chap_data])
    offset += 500

  #chap_list.sort() # sort numerically by chapter #

  return chap_data_list


