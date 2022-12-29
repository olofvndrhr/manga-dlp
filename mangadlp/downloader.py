import logging
import shutil
import sys
from pathlib import Path
from time import sleep
from typing import Union

import requests
from loguru import logger as log

from mangadlp import utils


# download images
def download_chapter(
    image_urls: list,
    chapter_path: Union[str, Path],
    download_wait: float,
) -> None:
    total_img = len(image_urls)
    for image_num, image in enumerate(image_urls, 1):
        # get image suffix
        image_suffix = str(Path(image).suffix) or ".png"
        # set image path
        image_path = Path(f"{chapter_path}/{image_num:03d}{image_suffix}")
        # show progress bar for default log level
        if logging.root.level == logging.INFO:
            utils.progress_bar(image_num, total_img)
        log.debug(f"Downloading image {image_num}/{total_img}")

        counter = 1
        while counter <= 3:
            try:
                r = requests.get(image, stream=True)
                if r.status_code != 200:
                    log.error(f"Request for image {image} failed, retrying")
                    raise ConnectionError
            except KeyboardInterrupt:
                log.critical("Stopping")
                sys.exit(1)
            except Exception as exc:
                if counter >= 3:
                    log.error("Maybe the MangaDex Servers are down?")
                    raise ConnectionError from exc
                sleep(download_wait)
                counter += 1
            else:
                break

        # write image
        try:
            with image_path.open("wb") as file:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, file)
        except Exception as exc:
            log.error("Can't write file")
            raise IOError from exc

        image_num += 1
        sleep(download_wait)
