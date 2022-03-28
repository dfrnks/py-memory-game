import torch
import datetime

from pathlib import Path

from src import MemoryGameEnv
from src import Memory
from src import MetricLogger


if __name__ == '__main__':
    env = MemoryGameEnv((4, 4))

    print(f"Using CUDA: {torch.cuda.is_available()}\n")

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    memory = Memory(state_dim=(env.action_space.n, env.action_space.n), action_dim=env.action_space.n, save_dir=save_dir)

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
