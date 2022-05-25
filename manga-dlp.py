import subprocess
import sys

from mangadlp.input import get_args

mangadlp_version = "2.1.2"


def get_input():
    print(f"manga-dlp version: {mangadlp_version}")
    print("Enter details of the manga you want to download:")
    while True:
        try:
            url_uuid = str(input("Url or UUID: "))
            readlist = str(input("List with links (optional): "))
            language = str(input("Language: ")) or "en"
            list_chapters = str(input("List chapters? y/N: "))
            if list_chapters.lower() != "y" or list_chapters.lower() != "yes":
                chapters = str(input("Chapters: "))
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            continue
        else:
            break

    args = [
        "python3",
        "manga-dlp.py",
        "-l",
        language,
        "-c",
        chapters,
    ]
    if url_uuid:
        args.append("-u")
        args.append(url_uuid)
    if readlist:
        args.append("--read")
        args.append(readlist)
    if list_chapters.lower() == "y" or list_chapters.lower() == "yes":
        args.append("--list")

    # start script again with the arguments
    subprocess.call(args)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_args()
    else:
        get_input()
