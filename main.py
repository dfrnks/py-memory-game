import sys
import logging
import random
import time
import uuid
import os
import threading
import datetime

from pathlib import Path

from src import PlayHistory, MemoryGameEnv

from play import play_random
from play import playing_manually_start
from play import play_with_network

logging.basicConfig(format='%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


if __name__ == "__main__":
    try:
        # playing_manually_start()

        play_random(4, 4, 1, 1)
        play_with_network(1)
    except KeyboardInterrupt:
        sys.exit()
