import torch
import random
import datetime

from pathlib import Path

from tqdm import tqdm

from src import MemoryGameEnv
from src import MemoryAgent
from src import MemoryNet
from src import MetricLogger


def training(agent, env, episodes=10000, comment=''):
    agent.load(agent.save_dir / 'memory_net.chkpt')

    logger = MetricLogger(agent.save_dir, tag='train', comment=comment)

    progress_bar = tqdm(range(episodes))
    for e in progress_bar:
        progress_bar.set_description_str(f'Training {e}')

        state = env.reset()

        done = False
        # Play the game!
        while not done:
            # Run agent on the state
            action = agent.act(state)

            # Agent performs action
            next_state, reward, done, info = env.step(action)

            # Remember
            agent.cache(state, next_state, action, reward, done)

            # Learn
            q, loss = agent.learn()

            # Logging
            logger.log_step(e, reward, loss, q, info['points'])

            # Update state
            state = next_state

        logger.log_episode(e)

        if e % 20 == 0:
            logger.record(
                progress_bar,
                episode=e,
                epsilon=agent.exploration_rate,
                step=agent.curr_step
            )

    logger.close()

    agent.save(agent.save_dir / 'memory_net.chkpt')


def eval(agent, env, episodes=10000, comment=''):
    agent.load(agent.save_dir / 'memory_net.chkpt')
    agent.exploration_rate = 0

    logger = MetricLogger(agent.save_dir, tag='eval', comment=comment)

    progress_bar = tqdm(range(episodes))
    for e in progress_bar:
        progress_bar.set_description_str(f'Eval {e}')

        state = env.reset()

        done = False
        # Play the game!
        while not done:
            # Run agent on the state
            action = agent.act(state)

            # Agent performs action
            next_state, reward, done, info = env.step(action)

            # Logging
            logger.log_step(e, reward, 0, 0, info['points'])

            # Update state
            state = next_state

        logger.log_episode(e)

        if e % 20 == 0:
            logger.record(
                progress_bar,
                episode=e,
                epsilon=agent.exploration_rate,
                step=agent.curr_step
            )

    logger.close()


def rand(agent, env, episodes=10000, comment=''):
    logger = MetricLogger(agent.save_dir, tag='random', comment=comment)

    progress_bar = tqdm(range(episodes))
    for e in progress_bar:
        progress_bar.set_description_str(f'Random playing {e}')

        env.reset()

        done = False
        # Play the game!
        while not done:
            # Run agent on the state
            action = random.randint(0, env.action_space.n - 1)

            # Agent performs action
            next_state, reward, done, info = env.step(action)

            # Logging
            logger.log_step(e, reward, 0, 0, info['points'])

        logger.log_episode(e)

        if e % 20 == 0:
            logger.record(
                progress_bar,
                episode=e,
                epsilon=agent.exploration_rate,
                step=agent.curr_step
            )

    logger.close()


if __name__ == '__main__':

    env = MemoryGameEnv((4, 4))

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    net = MemoryNet((env.action_space.n, env.action_space.n), env.action_space.n, device)

    agent = MemoryAgent(
        state_dim=(env.action_space.n, env.action_space.n),
        action_dim=env.action_space.n,
        net=net,
        save_dir=save_dir,
        lr=0.001,
        max_memory_size=1000000,
        batch_size=64,
        gamma=0.9,
        exploration_rate=1,
        exploration_rate_decay=0.99999999,
        exploration_rate_min=0.1,
        save_every=5e5,
        burnin=1e4,
        learn_every=3,
        sync_every=1e4,
    )

    training(agent, env, 100000)
