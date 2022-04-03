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
                f"\t--help -h           Help\n"
                f"\t--manually -m       Jogar um jogo vocẽ mesmo\n"
                f"\t--random -r         Jogar um jogo aleatoriamente pelo computadot\n"
                f"\t--network -n        Jogar um jogo pela rede neural\n"
                f"\t--m-rand 500        Multiplos jogos aleatoriamente. 500 = Numero de jogos.\n"
                f"\t--m-net 500         Multiplos jogos pela rede neural. 500 = Numero de jogos\n"
            )

        if len(args) > 1:
            if args[1] in ('-m', '--manually'):
                playing_manually_start()

            if args[1] in ('-r', '--random'):
                play_random(4, 4, 1, 1, True)

            if args[1] in ('-n', '--network'):
                play_with_network(1, True)

            if args[1] == '--m-rand':
                jogos = 500

                if len(args) > 2:
                    try:
                        jogos = int(args[2])
                    except Exception:
                        pass

                play_random(4, 4, jogos, 10, False)

            if args[1] == '--m-net':
                jogos = 500

                if len(args) > 2:
                    try:
                        jogos = int(args[2])
                    except Exception:
                        pass

                play_with_network(jogos, False)

    except KeyboardInterrupt:
        sys.exit()
