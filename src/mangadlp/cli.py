import sys
from pathlib import Path
from typing import Any, List

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
def readin_list(_ctx: click.Context, _param: str, value: str) -> List[str]:
    if not value:
        return []

    list_file = Path(value)
    click.echo(f"Reading in file '{list_file}'")
    try:
        url_str = list_file.read_text(encoding="utf-8")
        url_list = url_str.splitlines()
    except Exception as exc:
        msg = f"Reading in file '{list_file}'"
        raise click.BadParameter(msg) from exc

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
    type=click.Path(exists=True, dir_okay=False, path_type=str),
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
    "download_path",
    type=click.Path(exists=False, writable=True, path_type=Path),
    default="downloads",
    required=False,
    show_default=True,
    help="Download path",
)
@click.option(
    "-l",
    "--language",
    "language",
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
    "file_format",
    multiple=False,
    type=click.Choice(["cbz", "cbr", "zip", "pdf", ""], case_sensitive=False),
    default="cbz",
    required=False,
    show_default=True,
    help="Archive format to create. An empty string means don't archive the folder",
)
@click.option(
    "--name-format",
    "name_format",
    type=str,
    default="{default}",
    required=False,
    show_default=True,
    help="Naming format to use when saving chapters. See docs for more infos",
)
@click.option(
    "--name-format-none",
    "name_format_none",
    type=str,
    default="",
    required=False,
    show_default=True,
    help="String to use when the variable of the custom name format is empty",
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
    "download_wait",
    type=float,
    default=0.5,
    required=False,
    show_default=True,
    help="Time to wait for each picture to download in seconds(float)",
)
# hook options
@click.option(
    "--hook-manga-pre",
    "manga_pre_hook_cmd",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute before the manga download starts",
)
@click.option(
    "--hook-manga-post",
    "manga_post_hook_cmd",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute after the manga download finished",
)
@click.option(
    "--hook-chapter-pre",
    "chapter_pre_hook_cmd",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute before the chapter download starts",
)
@click.option(
    "--hook-chapter-post",
    "chapter_post_hook_cmd",
    type=str,
    default=None,
    required=False,
    show_default=True,
    help="Commands to execute after the chapter download finished",
)
@click.option(
    "--cache-path",
    "cache_path",
    type=click.Path(exists=False, writable=True, path_type=str),
    default=None,
    required=False,
    show_default=True,
    help="Where to store the cache-db. If no path is given, cache is disabled",
)
@click.option(
    "--add-metadata/--no-metadata",
    "add_metadata",
    is_flag=True,
    default=True,
    required=False,
    show_default=True,
    help="Enable/disable creation of metadata via ComicInfo.xml",
)
@click.pass_context
def main(ctx: click.Context, **kwargs: Any) -> None:
    """Script to download mangas from various sites."""
    url_uuid: str = kwargs.pop("url_uuid")
    read_mangas: List[str] = kwargs.pop("read_mangas")
    verbosity: int = kwargs.pop("verbosity")

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
        try:
            mdlp = app.MangaDLP(url_uuid=manga, **kwargs)
            mdlp.get_manga()
        except (KeyboardInterrupt, Exception) as exc:
            # if only a single manga is requested and had an error, then exit
            if len(requested_mangas) == 1:
                log.error(f"Error with manga: {manga}")
                sys.exit(1)
            # else continue with the other ones
            log.error(f"Skipping: {manga}. Reason={exc}")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
