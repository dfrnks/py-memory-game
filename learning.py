import torch
import datetime

from pathlib import Path

from tqdm import tqdm

from src import MemoryGameEnv
from src import MemoryAgent
from src import MetricLogger


def run(agent, episodes=10000):
    agent.load('checkpoints/memory_net.chkpt')

    logger = MetricLogger(agent.save_dir)

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

    agent.save('checkpoints/memory_net.chkpt')


if __name__ == '__main__':

    env = MemoryGameEnv((4, 4))

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    agent = MemoryAgent(
        state_dim=(env.action_space.n, env.action_space.n),
        action_dim=env.action_space.n,
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
        device="cuda" if torch.cuda.is_available() else "cpu"
    )

    run(agent, 100000)
