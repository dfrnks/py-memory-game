import sys
import logging
import random
import time
import uuid
import os
import threading

from src.memory_game import MemoryGame

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


def play(w, h, file_path, i, j):
    id = str(uuid.uuid4())
    start_time = time.time()

    game = MemoryGame(w, h)
    game.start()

    winning = False
    list = []
    jogadas = 0
    while not winning:
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)
        jogadas += 1

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
            str(jogadas),
            str(int(len(game.positions))),
            str(time.time())
        ])

        # if (time.time() - start_time) % 5:
        #     with open(file_path, mode='a', encoding='utf-8') as myfile:
        #         myfile.write('\n'.join(','.join(l) for l in list) + '\n')
        #     list = []
        # time.sleep(0.01)

        # if jogadas % 100000 == 0:
        #     print(f"Jogada {jogadas} - {len(game.positions)}")
        # game.print(f"Jogada {jogadas} - {len(game.positions)}")
        # print(f"Jogada {jogadas} - {len(game.positions)}")

    print("--- {}-{} item. {} seconds. {} Pontos ---".format(j, i, (time.time() - start_time), pontos))

    with open(file_path, mode='a', encoding='utf-8') as myfile:
        myfile.write('\n'.join(','.join(l) for l in list) + '\n')


if __name__ == "__main__":
    try:
        size = 10
        file_path = f'jogos-{size}x{size}-full.csv'

        if not os.path.exists(file_path):
            with open(file_path, mode='a', encoding='utf-8') as myfile:
                myfile.write('id,width,height,x,y,winning,acerto,pontos,jogada,possicoes,time\n')

        # play(size, size, file_path, 0, 0)

        for j in range(500):
            threads = [None] * 10
            results = []

            for i in range(len(threads)):
                threads[i] = threading.Thread(target=play, args=(size, size, file_path, i, j,))
                threads[i].start()

            for i in range(len(threads)):
                threads[i].join(600)

    except KeyboardInterrupt:
        sys.exit()
