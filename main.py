import sys
import logging
import random
import time
import uuid
import pandas as pd
import os
import threading

from src.memory_game import MemoryGame

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


def play(w, h, list, i, j):
    id = str(uuid.uuid4())
    start_time = time.time()

    game = MemoryGame(w, h, '0')
    game.start()

    winning = False
    while not winning:
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)

        winning, table, pontos, acerto = game.next(x, y)

        list.append([
            str(id),
            str(w),
            str(h),
            str(x),
            str(y),
            str(winning),
            str(acerto),
            str(pontos),
            str(time.time())
        ])

        # print("--- {} item. {} seconds. {} Pontos ---".format(i, (time.time() - start_time), pontos))
        # for line in table:
        #     logging.info('  '.join(map(str, line)))

    print("--- {}-{} item. {} seconds. {} Pontos ---".format(j, i, (time.time() - start_time), pontos))

    # return pd.DataFrame(l, columns=['id', 'width', 'height', 'x', 'y', 'winning', 'acerto', 'pontos', 'time'])


if __name__ == "__main__":
    try:
        size = 10
        file_path = f'jogos-{size}x{size}-full.csv'

        if not os.path.exists(file_path):
            with open(file_path, mode='a', encoding='utf-8') as myfile:
                myfile.write('id,width,height,x,y,winning,acerto,pontos,time\n')

        for j in range(100):
            threads = [None] * 50
            results = []

            for i in range(len(threads)):
                threads[i] = threading.Thread(target=play, args=(size, size, results, i, j,))
                threads[i].start()

            for i in range(len(threads)):
                threads[i].join(300)

            with open(file_path, mode='a', encoding='utf-8') as myfile:
                myfile.write('\n'.join(','.join(line) for line in results))

    except KeyboardInterrupt:
        sys.exit()
