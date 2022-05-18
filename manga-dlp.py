from mangadlp.input import get_args
import os
import sys

mangadlp_version = "2.1.1"


def get_input():
    print(f"Manga-DLP Version {mangadlp_version}")
    print("Enter details of the manga you want to download:")
    while True:
        try:
            url_uuid = str(input("Url or UUID: "))
            readlist = str(input("List with links (optional): "))
            language = str(input("Language: "))
            chapters = str(input("Chapters: "))
        except KeyboardInterrupt:
            exit(1)
        except:
            continue
        else:
            break
    args = [f"-l {language}", f"-c {chapters}"]
    if url_uuid:
        args.append(f"-u {url_uuid}")
    if readlist:
        args.append(f"--read {readlist}")

    # start script again with the arguments
    os.system(f"python3 manga-dlp.py {' '.join(args)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_args()
    else:
        get_input()
