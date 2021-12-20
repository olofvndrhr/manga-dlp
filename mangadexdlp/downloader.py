import shutil
import requests
from time import sleep
from pathlib import Path


def download_chapter(image_urls, chapter_path, verbose=False):
  # download images
  img_num = 1
  for img in image_urls:
    # set image path
    image_path = Path(f'{chapter_path}/{img_num:03d}')
    try:
      #print('Try getting ' + img)
      req = requests.get(img, stream = True)
    except:
      print(f'Request for image {img} failed, retrying')
      sleep(2)
      req = requests.get(img, stream = True)

    if req.status_code == 200:
      req.raw.decode_content = True
      with image_path.open('wb') as file:
        shutil.copyfileobj(req.raw, file)

      # verbose logging
      if verbose:
        print(f'  Downloaded image {img_num}')

      img_num += 1
      sleep(0.5)
    else:
      print('Image {img} could not be downloaded. Exiting')
      exit(1)
