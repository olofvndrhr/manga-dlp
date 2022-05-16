from pathlib import Path
from time import sleep
import shutil
import requests

import mangadlp.utils as utils


# download images
def download_chapter(image_urls, chapter_path, download_wait, verbose):
    total_img = len(image_urls)
    for img_num, img in enumerate(image_urls, 1):
        # set image path
        image_path = Path(f"{chapter_path}/{img_num:03d}")
        # show progress bar if verbose logging is not active
        if not verbose:
            utils.progress_bar(img_num, total_img, verbose)
        counter = 1
        while counter <= 3:
            try:
                r = requests.get(img, stream=True)
            except KeyboardInterrupt:
                print("ERR: Stopping")
                exit(1)
            except:
                if counter >= 3:
                    print("ERR: Maybe the MangaDex Servers are down?")
                    raise ConnectionError
                print(f"ERR: Request for image {img} failed, retrying")
                sleep(download_wait)
                counter += 1
            else:
                if r.status_code != 200:
                    print(f"ERR: Image {img} could not be downloaded. Retrying")
                    continue
                break

        # verbose logging
        if verbose:
            print(f"INFO: Downloaded image {img_num}/{total_img}")
        # write image
        try:
            with image_path.open("wb") as file:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, file)
        except:
            print("ERR: Can't write file")
            raise IOError

        img_num += 1
        sleep(download_wait)

    # if every image was downloaded and written successfully
    return True
