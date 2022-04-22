import os
import random
import time
import uuid
import threading
import datetime

from pathlib import Path

from src import PlayHistory
from src import MemoryGameEnv
from src import MemoryAgent


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


total_rewards = 0


def playing_manually(env):
    position = input("Enter the X Y position (ex: 12):")

    table, rewards, done, info = env.step(int(position))

    global total_rewards
    total_rewards += rewards

    cls()

    print(env.render(table))

    if done:
        cls()
        print(env.render())

        print(f"Gaming complete, Total points: {info['points']}, Total rewards: {total_rewards}")

        return

    playing_manually(env)


def playing_manually_start():
    # game_board_completed = [
    #     102, 107, 106, 107,
    #     104, 104, 100, 103,
    #     100, 105, 102, 101,
    #     105, 103, 106, 101
    # ]
    #
    # game_board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #
    # env = MemoryGameEnv((4, 4), game_board_completed, game_board)
    env = MemoryGameEnv((4, 4))
    env.reset()

    playing_manually(env)


def play_random_env(w, h, history: PlayHistory, i, j, show=False):
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

        if show:
            print(env.render())

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

    print("--- {}-{} item. {} seconds. {} jogadas, {} Pontos ---".format(j, i, (time.time() - start_time), n_games,
                                                                         info['points']))

    history.record(games)


def play_random(w, h, n, t, save_dir, show=False):
    """
    :param w: Largura
    :param h: Altura
    :param n: Numero de jogos
    :param t: Numero de threads, se t = 1 então não utiliza threads
    :return:
    """
    # save_dir = Path("history") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    # save_dir.mkdir(parents=True)

    save_dir = save_dir / 'history_random'
    save_dir = save_dir / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    history = PlayHistory(save_dir)

    for j in range(int(n / t)):
        if t == 1:
            play_random_env(w, h, history, 1, j, show)
        else:
            threads = [None] * t

            for i in range(len(threads)):
                threads[i] = threading.Thread(target=play_random_env, args=(w, h, history, i, j, show,))
                threads[i].start()

            for i in range(len(threads)):
                threads[i].join(600)


def play_with_network(agent, env, ep=1, show=False):
    # w = 4
    # h = 4
    # env = MemoryGameEnv((w, h))
    #
    # save_dir = Path("history_net") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    # save_dir.mkdir(parents=True)

    save_dir = agent.save_dir / 'history_net'
    save_dir = save_dir / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    history = PlayHistory(save_dir)

    agent.exploration_rate = 0

    for i in range(ep):

        state = env.reset()

        id = str(uuid.uuid4())
        start_time = time.time()

        done = False
        games = []
        n_games = 0
        info = []

        while not done:
            n_games += 1

            action = agent.act(state)

            next_state, reward, done, info = env.step(action)

            state = next_state

            if show:
                print(env.render())

            games.append([
                str(id),
                str(env.shape[0]),
                str(env.shape[1]),
                str(action),
                str(reward),
                str(done),
                str(n_games),
                str(info['points']),
                str(info['already_played']),
                str(info['num_errors']),
                str(time.time())
            ])

        print("--- {}-{} item. {} seconds. {} jogadas, {} Pontos ---".format(0, i, (time.time() - start_time), n_games,
                                                                             info['points']))

        history.record(games)
