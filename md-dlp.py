import mangadexdlp.main as Mangadex
import argparse

def main(args):
  Mangadex.mangadex_dlp(args.url,
                        args.chapter,
                        args.dest,
                        args.lang,
                        args.read,
                        args.list,
                        args.nocbz,
                        args.forcevol,
                        args.wait,
                        args.verbose)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Script to download mangas from Mangadex.org')
  parser.add_argument('-u', '--url',
                      dest='url',
                      required=False,
                      help='URL of the manga.',
                      action='store',
                      )
  parser.add_argument('-c', '--chapter',
                      dest='chapter',
                      required=False,
                      help='Chapter to download',
                      action='store',
                      )
  parser.add_argument('-d', '--destination',
                      dest='dest',
                      required=False,
                      help='Download path. Defaults to "<script_dir>/downloads',
                      action='store',
                      default='downloads',
                      )
  parser.add_argument('-l', '--language',
                      dest='lang',
                      required=False,
                      help='Manga language',
                      action='store',
                      default='en',
                      )
  parser.add_argument('--read',
                      dest='read',
                      required=False,
                      help='Path of file with manga links to download. One per line',
                      action='store',
                      )
  parser.add_argument('--list',
                      dest='list',
                      required=False,
                      help='List all available chapters',
                      action='store_true',
                      )
  parser.add_argument('--nocbz',
                      dest='nocbz',
                      required=False,
                      help='Dont pack it to a cbz archive. Defaults to false.',
                      action='store_true',
                      )
  parser.add_argument('--forcevol',
                      dest='forcevol',
                      required=False,
                      help='Force naming of volumes. For mangas where chapters reset each volume',
                      action='store_true',
                      )
  parser.add_argument('--wait',
                      dest='wait',
                      required=False,
                      type=float,
                      help='Time to wait for each picture to download in seconds(float). Defaults 0.5.',
                      )
  parser.add_argument('--verbose',
                      dest='verbose',
                      required=False,
                      help='Verbose logging. Defaults to false.',
                      action='store_true',
                      )

  #parser.print_help()
  args = parser.parse_args()

  main(args)

