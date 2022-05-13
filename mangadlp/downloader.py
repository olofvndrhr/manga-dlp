import shutil
from pathlib import Path
from time import sleep
import requests
import mangadlp.utils as utils

# download images
def download_chapter(image_urls, chapter_path, md_wait, md_verbose):
    img_num = 1
    total_img = len(image_urls)
    for img in image_urls:
        # set image path
        image_path = Path(f"{chapter_path}/{img_num:03d}")
        # show progress bar
        utils.progress_bar(img_num, total_img)
        try:
            # print('Try getting ' + img)
            req = requests.get(img, stream=True)
        except KeyboardInterrupt:
            print("ERR: Stopping")
            exit(1)
        except:
            print(f"ERR: Request for image {img} failed, retrying")
            sleep(md_wait)
            req = requests.get(img, stream=True)

        if req.status_code == 200:
            req.raw.decode_content = True
            with image_path.open("wb") as file:
                shutil.copyfileobj(req.raw, file)

            # verbose logging
            if md_verbose:
                print(f"INFO: Downloaded image {img_num}")

            img_num += 1
            sleep(md_wait)
        else:
            print(f"ERR: Image {img} could not be downloaded. Exiting")
            exit(1)
