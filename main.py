import sys
import logging

from src.memory_game import MemoryGame

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    try:
        game = MemoryGame(4, 4)
        game.start()
        # game.playing()

        for i in [
            [0, 0],
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 0],
            [1, 1],
        ]:
            _, o, p, _ = game.next(i[0], i[1])

            print(f'--------------- Pontos: {p}')

            for line in o:
                print('  '.join(map(str, line)))

    except KeyboardInterrupt:
        # quit
        sys.exit()
