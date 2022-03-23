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


def play(w, h, i):
    id = uuid.uuid4()
    start_time = time.time()

    game = MemoryGame(w, h, '0')
    game.start()

    winning = False
    l = []
    while not winning:
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)

        winning, table, pontos, acerto = game.next(x, y)

        l.append([
            id,
            w,
            h,
            x,
            y,
            winning,
            acerto,
            pontos,
            time.time(),
            table
        ])

    print("--- {} item. {} seconds. {} Pontos ---".format(i, (time.time() - start_time), pontos))

    return pd.DataFrame(l, columns=['id', 'width', 'height', 'x', 'y', 'winning', 'acerto', 'pontos', 'time', 'table'])


if __name__ == "__main__":
    try:
        if os.path.exists('jogos.csv'):
            file = pd.read_csv('jogos.csv')
        else:
            file = pd.DataFrame()

        for i in range(1000):
            df = play(8, 8, i)

            file = pd.concat([file, df], ignore_index=True, axis=0)

        file.to_csv('jogos.csv', index=False)

    except KeyboardInterrupt:
        sys.exit()
