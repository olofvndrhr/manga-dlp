import re
from datetime import datetime
from pathlib import Path
from typing import Any, List
from zipfile import ZipFile

import pytz
from loguru import logger as log


# create an archive of the chapter images
def make_archive(chapter_path: Path, file_format: str) -> None:
    zip_path = Path(f"{chapter_path}.zip")
    try:
        # create zip
        with ZipFile(zip_path, "w") as zipfile:
            for file in chapter_path.iterdir():
                zipfile.write(file, file.name)
        # rename zip to file format requested
        zip_path.replace(zip_path.with_suffix(file_format))
    except Exception as exc:
        log.error(f"Can't create '{file_format}' archive")
        raise exc


def make_pdf(chapter_path: Path) -> None:
    try:
        import img2pdf  # pylint: disable=import-outside-toplevel
    except Exception as exc:
        log.error("Cant import img2pdf. Please install it first")
        raise exc

    pdf_path = Path(f"{chapter_path}.pdf")
    images: List[str] = []
    for file in chapter_path.iterdir():
        images.append(str(file))
    try:
        pdf_path.write_bytes(img2pdf.convert(images))
    except Exception as exc:
        log.error("Can't create '.pdf' archive")
        raise exc


# create a list of chapters
def get_chapter_list(chapters: str, available_chapters: List[str]) -> List[str]:
    # check if there are available chapter
    chapter_list: List[str] = []
    for chapter in chapters.split(","):
        # check if chapter list is with volumes and ranges (forcevol)
        if "-" in chapter and ":" in chapter:
            # split chapters and volumes apart for list generation
            lower_num_fv: List[str] = chapter.split("-")[0].split(":")
            upper_num_fv: List[str] = chapter.split("-")[1].split(":")
            vol_fv: str = lower_num_fv[0]
            chap_beg_fv: int = int(lower_num_fv[1])
            chap_end_fv: int = int(upper_num_fv[1])
            # generate range inbetween start and end --> 1:1-1:3 == 1:1,1:2,1:3
            for chap in range(chap_beg_fv, chap_end_fv + 1):
                chapter_list.append(str(f"{vol_fv}:{chap}"))
        # no volumes, just chapter ranges
        elif "-" in chapter:
            lower_num: int = int(chapter.split("-")[0])
            upper_num: int = int(chapter.split("-")[1])
            # generate range inbetween start and end --> 1-3 == 1,2,3
            for chap in range(lower_num, upper_num + 1):
                chapter_list.append(str(chap))
        # check if full volume should be downloaded
        elif ":" in chapter:
            vol_num: str = chapter.split(":")[0]
            chap_num: str = chapter.split(":")[1]
            # select all chapters from the volume --> 1: == 1:1,1:2,1:3...
            if vol_num and not chap_num:
                regex: Any = re.compile(f"{vol_num}:[0-9]{{1,4}}")
                vol_list: List[str] = [n for n in available_chapters if regex.match(n)]
                chapter_list.extend(vol_list)
            else:
                chapter_list.append(chapter)
        # single chapters without a range given
        else:
            chapter_list.append(chapter)

    return chapter_list


# remove illegal characters etc
def fix_name(filename: str) -> str:
    filename = filename.encode(encoding="utf8", errors="ignore").decode(encoding="utf8")
    # remove illegal characters
    filename = re.sub(r'[/\\<>:;|?*!@"]', "", filename)
    # remove multiple dots
    filename = re.sub(r"([.]{2,})", ".", filename)
    # remove dot(s) at the beginning and end of the filename
    filename = re.sub(r"(^[.]+)|([.]+$)", "", filename)
    # remove trailing and beginning spaces
    filename = re.sub("([ \t]+$)|(^[ \t]+)", "", filename)

    log.debug(f"Input name='{filename}', Output name='{filename}'")
    return filename


# create name for chapter
def get_filename(
    manga_title: str,
    chapter_name: str,
    chapter_vol: str,
    chapter_num: str,
    forcevol: bool,
    name_format: str,
    name_format_none: str,
) -> str:
    # try to apply the custom format
    if name_format != "{default}":
        log.debug(f"Using custom name format: '{name_format}'")
        try:
            filename = name_format.format(
                manga_title=manga_title or name_format_none,
                chapter_name=chapter_name or name_format_none,
                chapter_vol=chapter_vol or name_format_none,
                chapter_num=chapter_num or name_format_none,
            )
        except Exception:
            log.warning("File format is not valid. Falling back to default")
        else:
            return filename

    # set vol to 0 if none found
    chapter_vol = chapter_vol or "0"

    # use default format
    log.debug("Using default name format")
    # if chapter is a oneshot
    if not chapter_num or "oneshot" in [chapter_name.lower(), chapter_num.lower()]:
        return "Oneshot"

    # if the chapter has no name
    if not chapter_name and forcevol:
        return f"Vol. {chapter_vol} Ch. {chapter_num}"
    if not chapter_name:
        return f"Ch. {chapter_num}"

    # if the chapter has a name
    # return with volume if option is set, else just the chapter num and name
    if forcevol:
        return f"Vol. {chapter_vol} Ch. {chapter_num} - {chapter_name}"

    return f"Ch. {chapter_num} - {chapter_name}"


def get_file_format(file_format: str) -> str:
    if not file_format:
        return ""

    if re.match(r"\.?[a-z0-9]+", file_format, flags=re.I):
        if file_format[0] != ".":
            file_format = f".{file_format}"
    else:
        log.error(f"Invalid file format: '{file_format}'")
        raise ValueError

    return file_format


def progress_bar(progress: float, total: float) -> None:
    time = datetime.now(tz=pytz.timezone("Europe/Zurich")).strftime("%Y-%m-%dT%H:%M:%S")
    percent = int(progress / (int(total) / 100))
    bar_length = 50
    bar_progress = int(progress / (int(total) / bar_length))
    bar_texture = "■" * bar_progress
    whitespace_texture = " " * (bar_length - bar_progress)
    if progress == total:
        full_bar = "■" * bar_length
        print(f"\r{time}{' '*6}| [BAR    ] ❙{full_bar}❙ 100%", end="\n")  # noqa
    else:
        print(  # noqa
            f"\r{time}{' '*6}| [BAR    ] ❙{bar_texture}{whitespace_texture}❙ {percent}%",
            end="\r",
        )
