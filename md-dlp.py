import mangadexdlp.main as Mangadex
import argparse

def main(args):

  Mangadex.mangadex_dlp(args.url, args.chapter, args.dest, args.lang, args.list, args.nocbz)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Script to download mangas from Mangadex.org')
  parser.add_argument('-u', '--url',
                      dest='url',
                      required=True,
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
                      help='Download path',
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
  parser.add_argument('--list',
                      dest='list',
                      required=False,
                      help='List all available chapters',
                      action='store_true',
                      )
  parser.add_argument('--nocbz',
                      dest='nocbz',
                      required=False,
                      help='Dont pack it to a cbz archive',
                      action='store_true',
                      )

  #parser.print_help()
  args = parser.parse_args()

  main(args)

