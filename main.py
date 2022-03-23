import sys
import logging
import random
import time
import uuid
import pandas as pd
import os

from src.memory_game import MemoryGame

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


def play(i):
    w = 8
    h = 8
    id = uuid.uuid4()
    start_time = time.time()
    df = pd.DataFrame(columns=['id', 'width', 'height', 'x', 'y', 'winning', 'acerto', 'pontos'])

    game = MemoryGame(w, h)
    game.start()

    winning = False
    while not winning:
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)

        winning, o, p, a = game.next(x, y)

        gInfo = pd.DataFrame({
            'id': [id],
            'time': [time.time()],
            'width': [w],
            'height': [h],
            'x': [x],
            'y': [y],
            'winning': [winning],
            'acerto': [a],
            'pontos': [p]
        })

        df = pd.concat([df, gInfo], ignore_index=True, axis=0)

    if os.path.exists('jogos.csv'):
        file = pd.read_csv('jogos.csv')
    else:
        file = pd.DataFrame()

    df = pd.concat([file, df], ignore_index=True, axis=0)

    df.to_csv('jogos.csv', index=False)

    print("--- {} item. {} seconds. {} Pontos ---".format(i, (time.time() - start_time), p))


if __name__ == "__main__":
    try:
        for i in range(100):
            play(i)
        # game = MemoryGame(4, 4)
        # game.start()
        # # game.playing()
        #
        # for i in [
        #     [0, 0],
        #     [0, 1],
        #     [0, 2],
        #     [0, 3],
        #     [1, 0],
        #     [1, 1],
        # ]:
        #     f, o, p, a = game.next(i[0], i[1])
        #
        #     print(f'-- Finished: {f} - Acertou: {a} - Pontos: {p}')
        #
        #     for line in o:
        #         print('  '.join(map(str, line)))

    except KeyboardInterrupt:
        sys.exit()
