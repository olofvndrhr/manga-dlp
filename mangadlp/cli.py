from pathlib import Path

import click
from click_option_group import (
    MutuallyExclusiveOptionGroup,
    RequiredMutuallyExclusiveOptionGroup,
    optgroup,
)
from loguru import logger as log

from mangadlp import app
from mangadlp.__about__ import __version__
from mangadlp.logger import prepare_logger


# read in the list of links from a file
def readin_list(_, __, value) -> list:
    if not value:
        return []

    list_file = Path(value)
    click.echo(f"Reading in file '{list_file}'")
    try:
        url_str = list_file.read_text(encoding="utf-8")
        url_list = url_str.splitlines()
    except Exception as exc:
        raise click.BadParameter("Can't get links from the file") from exc

    # filter empty lines and remove them
    filtered_list = list(filter(len, url_list))
    click.echo(f"Mangas from list: {filtered_list}")

    return filtered_list


@click.command(context_settings={"max_content_width": 150})
@click.help_option()
@click.version_option(version=__version__, package_name="manga-dlp")
# manga selection
@optgroup.group("source", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option(
    "-u",
    "--url",
    "--uuid",
    "url_uuid",
    type=str,
    default=None,
    show_default=True,
    help="URL or UUID of the manga",
)
@optgroup.option(
    "--read",
    "read_mangas",
    is_eager=True,
    callback=readin_list,
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    show_default=True,
    help="Path of file with manga links to download. One per line",
)
# logging options
@optgroup.group("verbosity", cls=MutuallyExclusiveOptionGroup)
@optgroup.option(
    "--loglevel",
    "verbosity",
    type=int,
    default=None,
    show_default=True,
    help="Custom log level",
)
@optgroup.option(
    "--warn",
    "verbosity",
    flag_value=30,
    default=None,
    show_default=True,
    help="Only log warnings and higher",
)
@optgroup.option(
    "--debug",
    "verbosity",
    flag_value=10,
    default=None,
    show_default=True,
    help="Debug logging. Log EVERYTHING",
)
# other options
@click.option(
    "-c",
    "--chapters",
    "chapters",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Chapters to download",
)
@click.option(
    "-p",
    "--path",
    "path",
    type=click.Path(exists=False),
    default="downloads",
    required=False,
    show_default=True,
    help="Download path",
)
@click.option(
    "-l",
    "--language",
    "lang",
    type=str,
    default="en",
    required=False,
    show_default=True,
    help="Manga language",
)
@click.option(
    "--list",
    "list_chapters",
    is_flag=True,
    default=False,
    required=False,
    show_default=True,
    help="List all available chapters",
)
@click.option(
    "--format",
    "chapter_format",
    type=str,
    default="cbz",
    required=False,
    show_default=True,
    help="Archive format to create. An empty string means dont archive the folder",
)
@click.option(
    "--forcevol",
    "forcevol",
    is_flag=True,
    default=False,
    required=False,
    show_default=True,
    help="Force naming of volumes. For mangas where chapters reset each volume",
)
@click.option(
    "--wait",
    "wait_time",
    type=float,
    default=0.5,
    required=False,
    show_default=True,
    help="Time to wait for each picture to download in seconds(float)",
)
# hook options
@click.option(
    "--hook-manga-pre",
    "hook_manga_pre",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute before the manga download starts",
)
@click.option(
    "--hook-manga-post",
    "hook_manga_post",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute after the manga download finished",
)
@click.option(
    "--hook-chapter-pre",
    "hook_chapter_pre",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute before the chapter download starts",
)
@click.option(
    "--hook-chapter-post",
    "hook_chapter_post",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute after the chapter download finished",
)
@click.pass_context
def main(
    ctx: click.Context,
    url_uuid: str,
    read_mangas: list,
    verbosity: int,
    chapters: str,
    path: str,
    lang: str,
    list_chapters: bool,
    chapter_format: str,
    forcevol: bool,
    wait_time: float,
    hook_manga_pre: str,
    hook_manga_post: str,
    hook_chapter_pre: str,
    hook_chapter_post: str,
):  # pylint: disable=too-many-locals

    """
    Script to download mangas from various sites

    """

    # set log level to INFO if not set
    if not verbosity:
        verbosity = 20

    # set loglevel and log format
    prepare_logger(verbosity)

    # list all params
    log.debug(ctx.params)

    # all request mangas
    requested_mangas = [url_uuid] if url_uuid else read_mangas

    for manga in requested_mangas:
        mdlp = app.MangaDLP(
            url_uuid=manga,
            language=lang,
            chapters=chapters,
            list_chapters=list_chapters,
            file_format=chapter_format,
            forcevol=forcevol,
            download_path=path,
            download_wait=wait_time,
            manga_pre_hook_cmd=hook_manga_pre,
            manga_post_hook_cmd=hook_manga_post,
            chapter_pre_hook_cmd=hook_chapter_pre,
            chapter_post_hook_cmd=hook_chapter_post,
        )
        mdlp.get_manga()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
