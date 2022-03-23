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


def play():
    w = 8
    h = 8
    id = uuid.uuid4()
    start_time = time.time()
    df = pd.DataFrame(columns=['id', 'width', 'height', 'x', 'y', 'winning', 'acerto', 'pontos'])

    if os.path.exists('jogos.csv'):
        df = pd.read_csv('jogos.csv')

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

        # print(f'-- Finished: {winning} - Acertou: {a} - Pontos: {p}')
        #
        # for line in o:
        #     print('  '.join(map(str, line)))

        # time.sleep(0.4)

    df.to_csv('jogos.csv', index=False)

    print(df[df['id'] == id]['acerto'].value_counts())

    print("--- {} seconds. {} Pontos ---".format((time.time() - start_time), p))


if __name__ == "__main__":
    try:
        play()
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
        # quit
        sys.exit()
