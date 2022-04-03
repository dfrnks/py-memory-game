import sys
import logging
import warnings


def warn(*args, **kwargs):
    pass


warnings.warn = warn

from play import play_random
from play import playing_manually_start
from play import play_with_network

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    try:

        args = sys.argv

        if len(args) < 2 or args[1] in ('-h', '--help'):
            print(
                f"Informe alguma opção:\n"
                f"\t--help -h\n"
                f"\t--manually -m\n"
                f"\t--random -r\n"
                f"\t--network -n\n"
            )

        if args[1] in ('-m', '--manually'):
            playing_manually_start()

        if args[1] in ('-r', '--random'):
            play_random(4, 4, 1, 1)

        if args[1] in ('-n', '--network'):
            play_with_network(1)

    except KeyboardInterrupt:
        sys.exit()
