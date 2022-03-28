import os
import sys
import logging
import random
import time
import uuid
import threading
import datetime


from pathlib import Path

from src import PlayHistory
from src import MemoryGameEnv
from src import Memory


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def playing_manually(env):
    position = input("Enter the X Y position (ex: 12):")

    table, rewards, done, info = env.step(int(position))

    cls()

    print(env.render(table))

    if done:
        cls()
        print(env.render())

        print(f"Gaming complete, Total points: {info['points']}")

        return

    playing_manually(env)


def playing_manually_start():
    env = MemoryGameEnv((4, 4))
    env.reset()

    playing_manually(env)


def play_random_env(w, h, history: PlayHistory, i, j):
    env = MemoryGameEnv((w, h))
    env.reset()

    id = str(uuid.uuid4())
    start_time = time.time()

    done = False
    games = []
    n_games = 0
    info = []

    while not done:
        n_games += 1

        action = random.randint(0, env.action_space.n - 1)

        game_board, reward, done, info = env.step(action)

        games.append([
            str(id),
            str(w),
            str(h),
            str(action),
            str(reward),
            str(done),
            str(n_games),
            str(info['points']),
            str(info['already_played']),
            str(info['num_errors']),
            str(time.time())
        ])

    print("--- {}-{} item. {} seconds. {} Pontos ---".format(j, i, (time.time() - start_time), info['points']))

    history.record(games)


def play_random(w, h, n, t):
    """
    :param w: Largura
    :param h: Altura
    :param n: Numero de jogos
    :param t: Numero de threads, se t = 1 então não utiliza threads
    :return:
    """
    save_dir = Path("history") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)
    history = PlayHistory(save_dir)

    for j in range(int(n/t)):
        if t == 1:
            play_random_env(w, h, history, 1, j)
        else:
            threads = [None] * t

            for i in range(len(threads)):
                threads[i] = threading.Thread(target=play_random_env, args=(w, h, history, i, j,))
                threads[i].start()

            for i in range(len(threads)):
                threads[i].join(600)


def play_with_network(ep=1):
    w = 4
    h = 4
    env = MemoryGameEnv((w, h))

    save_dir = Path("history_net") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    history = PlayHistory(save_dir)

    memory = Memory(state_dim=(env.action_space.n, env.action_space.n), action_dim=env.action_space.n, save_dir=save_dir)

    memory.load('checkpoints/memory_net.chkpt')

    for i in range(ep):

        state = env.reset()

        id = str(uuid.uuid4())
        start_time = time.time()

        done = False
        games = []
        n_games = 0
        info = []

        while not done:
            action = memory.act(state)

            next_state, reward, done, info = env.step(action)

            state = next_state

            games.append([
                str(id),
                str(w),
                str(h),
                str(action),
                str(reward),
                str(done),
                str(n_games),
                str(info['points']),
                str(info['already_played']),
                str(info['num_errors']),
                str(time.time())
            ])

        print("--- {}-{} item. {} seconds. {} Pontos ---".format(0, i, (time.time() - start_time), info['points']))

        history.record(games)