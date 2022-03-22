import sys
import logging

from src.memory_game import MemoryGame

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    try:
        logging.info("Init game...")

        game = MemoryGame(3, 4)
        game.start()
    except KeyboardInterrupt:
        # quit
        sys.exit()
