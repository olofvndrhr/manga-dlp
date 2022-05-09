import re
import shutil
from pathlib import Path
from zipfile import ZipFile


# create a cbz archive
def make_archive(chapter_path):
    image_folder = Path(chapter_path)
    zip_path = Path(f"{chapter_path}.zip")
    with ZipFile(f"{image_folder}.zip", "w") as zip_archive:
        for file in image_folder.iterdir():
            zip_archive.write(file, file.name)

    zip_path.rename(zip_path.with_suffix(".cbz"))
    shutil.rmtree(image_folder)


# check if the file already exists
def check_existence(chapter_path, manga_nocbz):
    # check for folder if option nocbz is given. if nocbz is not given, the folder will be overwritten
    chapter_path = Path(chapter_path)
    cbz_path = chapter_path.parent / f"{chapter_path.name}.cbz"
    if manga_nocbz and chapter_path.exists():
        return True
    # check for cbz archive
    elif not manga_nocbz and cbz_path.exists():
        return True
    else:
        return False


# create a list of chapters
def get_chapter_list(chapters):
    chapter_list = []
    for chapter in chapters.split(","):
        if "-" in chapter and ":" in chapter:
            lower = chapter.split("-")[0].split(":")
            upper = chapter.split("-")[1].split(":")
            for n in range(int(lower[1]), int(upper[1]) + 1):
                chapter_list.append(str(f"{lower[0]}:{n}"))
        elif "-" in chapter:
            lower = chapter.split("-")[0]
            upper = chapter.split("-")[1]
            for n in range(int(lower), int(upper) + 1):
                chapter_list.append(str(n))
        else:
            chapter_list.append(chapter)

    return chapter_list


# remove illegal characters etc
def fix_name(filename):
    # remove illegal characters
    filename = re.sub("[\\\/\<\>\:\;\|\?\*\!\@]", "", filename)
    # remove multiple dots
    filename = re.sub("([\.]{2,})", ".", filename)
    # remove dot(s) at the beginning and end of the filename
    filename = re.sub("(^[\.]{1,})|([\.]{1,}$)", "", filename)
    # remove trailing and beginning spaces
    filename = re.sub("([ \t]+$)|(^[ \t]+)", "", filename)

    return filename


# create name for chapter
def get_filename(chapter_name, chapter_vol, chapter_num, manga_forcevol):
    # filename for chapter
    if chapter_name == "Oneshot" or chapter_num == "Oneshot":
        chapter_filename = "Oneshot"
    elif not chapter_name and manga_forcevol:
        chapter_filename = f"Vol. {chapter_vol} Ch. {chapter_num}"
    elif not chapter_name:
        chapter_filename = f"Ch. {chapter_num}"
    elif manga_forcevol:
        chapter_filename = f"Vol. {chapter_vol} Ch. {chapter_num} - {chapter_name}"
    else:
        chapter_filename = f"Ch. {chapter_num} - {chapter_name}"

    return chapter_filename
