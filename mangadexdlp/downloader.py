import shutil
import requests
from time import sleep
from pathlib import Path


def download_chapter(image_urls, chapter_path):
  # download images
  for img in image_urls:
    # set image path
    img_num = 1
    image_path = chapter_path / img_num

    try:
      req = requests.get(img, stream = True)
    except:
      print('Request failed, retrying')
      sleep(2)
      req = requests.get(img, stream = True)

    if req.status_code == 200:
      req.raw.decode_content = True
      with image_path.open('wb') as file:
        shutil.copyfileobj(req.raw, file)

      print(f'Downloaded image {img_num}')
      img_num += 1
    else:
      print('Image could not be downloaded. Exiting')
      exit(1)
