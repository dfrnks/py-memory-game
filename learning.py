import torch
import datetime

from pathlib import Path

from tqdm import tqdm

from src import MemoryGameEnv
from src import MemoryAgent
from src import MetricLogger


def run(episodes=10000):
    env = MemoryGameEnv((4, 4))

    print(f"Using CUDA: {torch.cuda.is_available()}\n")

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    agent = MemoryAgent(
        state_dim=(env.action_space.n, env.action_space.n),
        action_dim=env.action_space.n,
        save_dir=save_dir,
        batch_size=32
    )

    agent.load('checkpoints/memory_net.chkpt')

    logger = MetricLogger(save_dir)

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
    run(5000)
