import re
import shutil
from pathlib import Path
from zipfile import ZipFile


# create a cbz archive
def make_archive(chapter_path, file_format):
    # set manga format suffix
    if file_format and "." not in file_format:
        file_format = f".{file_format}"
    image_folder = Path(chapter_path)
    zip_path = Path(f"{chapter_path}.zip")
    if not image_folder.exists():
        print(f"ERR: Folder: {image_folder} does not exist")
        return False
    with ZipFile(f"{image_folder}.zip", "w") as zip_archive:
        for file in image_folder.iterdir():
            zip_archive.write(file, file.name)
    zip_path.rename(zip_path.with_suffix(file_format))
    shutil.rmtree(image_folder)

    return True


# check if the file already exists
def check_existence(chapter_path, file_format):
    # set manga format suffix
    if file_format and "." not in file_format:
        file_format = f".{file_format}"
    # check for folder if no format is given (empty string)
    # if no format is given, the folder will be overwritten if it exists
    chapter_path = Path(chapter_path).with_suffix(file_format)
    if chapter_path.exists():
        return True
    else:
        return False


# create a list of chapters
def get_chapter_list(chapters):
    chapter_list = []
    for chapter in chapters.split(","):
        # check if chapter list is with volumes and ranges
        if "-" in chapter and ":" in chapter:
            # split chapters and volumes apart for list generation
            lower = chapter.split("-")[0].split(":")
            upper = chapter.split("-")[1].split(":")
            # generate range inbetween start and end --> 1-3 == 1,2,3
            for n in range(int(lower[1]), int(upper[1]) + 1):
                chapter_list.append(str(f"{lower[0]}:{n}"))
        # no volumes, just chapter ranges
        elif "-" in chapter:
            lower = chapter.split("-")[0]
            upper = chapter.split("-")[1]
            # generate range inbetween start and end --> 1-3 == 1,2,3
            for n in range(int(lower), int(upper) + 1):
                chapter_list.append(str(n))
        # single chapters without a range given
        else:
            chapter_list.append(chapter)

    return chapter_list


# remove illegal characters etc
def fix_name(filename):
    # remove illegal characters
    filename = re.sub('[\\\/\<\>\:\;\|\?\*\!\@"]', "", filename)
    # remove multiple dots
    filename = re.sub("([\.]{2,})", ".", filename)
    # remove dot(s) at the beginning and end of the filename
    filename = re.sub("(^[\.]{1,})|([\.]{1,}$)", "", filename)
    # remove trailing and beginning spaces
    filename = re.sub("([ \t]+$)|(^[ \t]+)", "", filename)

    return filename


# create name for chapter
def get_filename(chapter_name, chapter_vol, chapter_num, forcevol):
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


def progress_bar(progress, total):
    percent = int(progress / (int(total) / 100))
    bar_length = 50
    bar_progress = int(progress / (int(total) / bar_length))
    bar_texture = "■" * bar_progress
    whitespace_texture = " " * (bar_length - bar_progress)
    if progress == total:
        print(f"\r❙{bar_texture}{whitespace_texture}❙ 100%", end="\n")
    else:
        print(f"\r❙{bar_texture}{whitespace_texture}❙ {percent}%", end="\r")
