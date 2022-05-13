import shutil
from pathlib import Path
from time import sleep
import requests
import mangadlp.utils as utils

# download images
def download_chapter(image_urls, chapter_path, download_wait, verbose):
    img_num = 1
    total_img = len(image_urls)
    for img in image_urls:
        # set image path
        image_path = Path(f"{chapter_path}/{img_num:03d}")
        # show progress bar
        utils.progress_bar(img_num, total_img)
        try:
            # print('Try getting ' + img)
            r = requests.get(img, stream=True)
        except KeyboardInterrupt:
            print("ERR: Stopping")
            exit(1)
        except:
            print(f"ERR: Request for image {img} failed, retrying")
            sleep(download_wait)
            req = requests.get(img, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True
            with image_path.open("wb") as file:
                shutil.copyfileobj(r.raw, file)

            # verbose logging
            if verbose:
                print(f"INFO: Downloaded image {img_num}")

            img_num += 1
            sleep(download_wait)
        else:
            print(f"ERR: Image {img} could not be downloaded. Exiting")
            exit(1)
