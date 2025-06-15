# Hooks

## Available hooks

You can run custom hooks with manga-dlp for specific events.
They are run with the `subproccess.run` function, so they get run directly by your operating system.

The available hook events are:

- **Pre Manga** -> Before anything gets downloaded
- **Pre Chapter** -> Before the chapter gets downloaded
- **Post Manga** -> After the manga is done. (All specified chapters were downloaded)
- **Post Chapter** -> After each chapter was downloaded (and formatted if specified)

Each of these hooks can be set with a specific flag:

- `--hook-pre-manga` -> Pre Manga hook
- `--hook-pre-chapter` -> Pre Chapter hook
- `--hook-post-manga` -> Post Manga hook
- `--hook-post-chapter` -> Post Chapter hook

**Example:**

```sh
manga-dlp -u <some url> -c 1 --hook-post-manga <some command>

# echo "abc" to stdout
manga-dlp -u <some url> -c 1 --hook-post-manga "echo abc"

# echo the manga name to stdout

manga-dlp -u <some url> -c 1 --hook-post-manga "echo ${MDLP_MANGA_TITLE}"
```

## Env Variables

All hooks are exposed to a variety of environment variables with infos about the manga/chapter currently downloading.

All available env variables are listed below with the example
for [this](https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona) manga:

> Command
>
> used: `python3 manga-dlp.py -u https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona -c 1`

**General:**

- `MDLP_HOOK_TYPE` -> manga_pre / manga_post / chapter_pre / chapter_post
- `MDLP_STATUS` -> starting / success / error / none
- `MDLP_REASON` -> none or the reason of the status

**Manga hooks:**

- `MDLP_API` -> Mangadex
- `MDLP_MANGA_URL_UUID` -> https://mangadex.org/title/7b0fbb36-7e17-4709-b616-742005b7e0e3/yona-yona-yona
- `MDLP_MANGA_UUID` -> 0aea9f43-d4a9-4bf7-bebc-550a512f9b95
- `MDLP_MANGA_TITLE` -> Yona Yona Yona
- `MDLP_LANGUAGE` -> en
- `MDLP_TOTAL_CHAPTERS` -> 158
- `MDLP_CHAPTERS_TO_DOWNLOAD` -> ['1']
- `MDLP_FILE_FORMAT` -> .cbz
- `MDLP_FORCEVOL` -> False
- `MDLP_DOWNLOAD_PATH` -> downloads
- `MDLP_MANGA_PATH` -> downloads/Yona Yona Yona

**Chapter hooks (extends Manga hooks env variables):**

- `MDLP_CHAPTER_FILENAME` -> Ch. 1
- `MDLP_CHAPTER_PATH` -> downloads/Yona Yona Yona/Ch. 1
- `MDLP_CHAPTER_ARCHIVE_PATH` -> downloads/Yona Yona Yona/Ch. 1.cbz
- `MDLP_CHAPTER_UUID` -> b7cba066-0b45-4d88-be08-89240841b4f7
- `MDLP_CHAPTER_VOLUME` -> 1
- `MDLP_CHAPTER_NUMBER` -> 1
- `MDLP_CHAPTER_NAME` -> `empty string`
