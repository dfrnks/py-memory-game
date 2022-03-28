from src.memory_env import MemoryGameEnv
from src.memory_play import Memory
from src.logging import MetricLogger

import torch
from pathlib import Path
import datetime
import random, os, time


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def playing(env):
    position = input("Enter the X Y position (ex: 12):")

    table, rewards, done, info = env.step(int(position))

    print(env.render(table))
    if done:
        print(env.render())

        print(f"Gaming complete, Total points: {info['points']}")

        return

    playing(env)


if __name__ == '__main__':
    env = MemoryGameEnv((4, 4))

    use_cuda = torch.cuda.is_available()
    print(f"Using CUDA: {use_cuda}")
    print()

    device = torch.device('cpu')
    if use_cuda:
        device = torch.device('cuda')

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    memory = Memory(state_dim=(1, 16, 16), action_dim=env.action_space.n, save_dir=save_dir)

    memory.load('checkpoints/memory_net.chkpt')

    logger = MetricLogger(save_dir)

    episodes = 10000
    for e in range(episodes):

        state = env.reset()

        # Play the game!
        while True:

            # Run agent on the state
            action = memory.act(state)

            # Agent performs action
            next_state, reward, done, info = env.step(action)

            # Remember
            memory.cache(state, next_state, action, reward, done)

            # Learn
            q, loss = memory.learn()

            # Logging
            logger.log_step(reward, loss, q)

            # Update state
            state = next_state

            # Check if end of game
            if done:
                break

        logger.log_episode()

        if e % 20 == 0:
            logger.record(episode=e, epsilon=memory.exploration_rate, step=memory.curr_step)

    memory.save('checkpoints/memory_net.chkpt')
