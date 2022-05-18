import re
from pathlib import Path
from zipfile import ZipFile


# create an archive of the chapter images
def make_archive(chapter_path: Path, file_format: str) -> None:
    zip_path = Path(f"{chapter_path}.zip")
    try:
        # create zip
        with ZipFile(zip_path, "w") as zipfile:
            for file in chapter_path.iterdir():
                zipfile.write(file, file.name)
        # rename zip to file format requested
        zip_path.rename(zip_path.with_suffix(file_format))
    except:
        raise IOError


def make_pdf(chapter_path: Path) -> None:
    try:
        import img2pdf
    except:
        print("Cant import img2pdf. Please install it first")
        raise ImportError

    pdf_path = Path(f"{chapter_path}.pdf")
    images = []
    for file in chapter_path.iterdir():
        images.append(str(file))
    try:
        pdf_path.write_bytes(img2pdf.convert(images))
    except:
        print("ERR: Can't create '.pdf' archive")
        raise IOError


# create a list of chapters
def get_chapter_list(chapters: str, available_chapters: list = None) -> list:
    chapter_list = []
    for chapter in chapters.split(","):
        # check if chapter list is with volumes and ranges
        if "-" in chapter and ":" in chapter:
            # split chapters and volumes apart for list generation
            lower_num = chapter.split("-")[0].split(":")
            upper_num = chapter.split("-")[1].split(":")
            vol = lower_num[0]
            chap_beg = int(lower_num[1])
            chap_end = int(upper_num[1])
            # generate range inbetween start and end --> 1:1-1:3 == 1:1,1:2,1:3
            for chap in range(chap_beg, chap_end + 1):
                chapter_list.append(str(f"{vol}:{chap}"))
        # no volumes, just chapter ranges
        elif "-" in chapter:
            lower_num = int(chapter.split("-")[0])
            upper_num = int(chapter.split("-")[1])
            # generate range inbetween start and end --> 1-3 == 1,2,3
            for chap in range(lower_num, upper_num + 1):
                chapter_list.append(str(chap))
        # check if full volume should be downloaded
        elif ":" in chapter:
            vol = chapter.split(":")[0]
            chap = chapter.split(":")[1]
            # select all chapters from the volume --> 1: == 1:1,1:2,1:3...
            if vol and not chap:
                regex = re.compile(f"{vol}:[0-9]{{1,4}}")
                vol_list = [n for n in available_chapters if regex.match(n)]
                chapter_list.extend(vol_list)
            else:
                chapter_list.append(chapter)
        # single chapters without a range given
        else:
            chapter_list.append(chapter)

    return chapter_list


# remove illegal characters etc
def fix_name(filename: str) -> str:
    # remove illegal characters
    filename = re.sub(r'[/\\<>:;|?*!@"]', "", filename)
    # remove multiple dots
    filename = re.sub(r"([.]{2,})", ".", filename)
    # remove dot(s) at the beginning and end of the filename
    filename = re.sub(r"(^[.]+)|([.]+$)", "", filename)
    # remove trailing and beginning spaces
    filename = re.sub("([ \t]+$)|(^[ \t]+)", "", filename)

    return filename


# create name for chapter
def get_filename(
    chapter_name: str, chapter_vol: str, chapter_num: str, forcevol: bool
) -> str:
    # if chapter is a oneshot
    if chapter_name == "Oneshot" or chapter_num == "Oneshot":
        return "Oneshot"
    # if the chapter has no name
    if not chapter_name:
        return (
            f"Vol. {chapter_vol} Ch. {chapter_num}"
            if forcevol
            else f"Ch. {chapter_num}"
        )
    # if the chapter has a name
    # return with volume if option is set, else just the chapter num and name
    return (
        f"Vol. {chapter_vol} Ch. {chapter_num} - {chapter_name}"
        if forcevol
        else f"Ch. {chapter_num} - {chapter_name}"
    )


def progress_bar(progress: float, total: float) -> None:
    percent = int(progress / (int(total) / 100))
    bar_length = 50
    bar_progress = int(progress / (int(total) / bar_length))
    bar_texture = "■" * bar_progress
    whitespace_texture = " " * (bar_length - bar_progress)
    if progress == total:
        full_bar = "■" * bar_length
        print(f"\r❙{full_bar}❙ 100%", end="\n")
    else:
        print(f"\r❙{bar_texture}{whitespace_texture}❙ {percent}%", end="\r")
