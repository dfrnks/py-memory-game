import torch
import datetime

from pathlib import Path

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
        burnin=2,
        learn_every=2,
        batch_size=2
    )

    agent.load('checkpoints/memory_net.chkpt')

    logger = MetricLogger(save_dir)

    for e in range(episodes):

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
            logger.log_step(reward, loss, q)

            # Update state
            state = next_state

        logger.log_episode()

        if e % 20 == 0:
            logger.record(
                episode=e,
                epsilon=agent.exploration_rate,
                step=agent.curr_step
            )

    agent.save('checkpoints/memory_net.chkpt')


if __name__ == '__main__':
    run(1)
