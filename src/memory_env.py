import copy
import random
import numpy as np

from io import StringIO
from gym import Env
from gym import spaces
from typing import Optional
from contextlib import closing


def createGameBoard(width, height, character):
    """
    Create two game boards for a new Game
    The firts game board is created are the completed game board
    The second are the game board that the player will use

    :param width:
    :param height:
    :param character:
    :return:
    """
    el = (width * height) / 2

    assert el % 2 == 0
    assert el > 2

    used = {}

    def getNewObj(e):
        obj = random.randint(100, 99 + e)

        used[obj] = 1 if obj not in used else used[obj] + 1

        if used[obj] > 2:
            return getNewObj(e)

        return obj

    game_board_completed = [getNewObj(el) for w in range(width * height)]
    game_board = [character for w in range(width * height)]

    return game_board_completed, game_board


class MemoryGameEnv(Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, shape=(8, 8), game_board_completed=None, game_board=None):
        self.shape = shape
        self.r_game_board_completed = game_board_completed
        self.r_game_board = game_board

        self.reward_range = (-float("inf"), float("inf"))

        self.nS = np.prod(self.shape)

        self.action_space = spaces.Discrete(int(self.nS))

        self.game_board_completed = []
        self.game_board = []
        self.game_board_copy = []
        self.already_played = []
        self.points = 0
        self.num_errors = 0
        self.correct = 0
        self.last_played = None

        self.rewards = {
            'first': 2,
            'correct': 5, # Acumulative
            'wrong': -5,
            'already_played_last': -10,
            'already_played': -2
        }

    def step(self, action) -> ([], int, bool, dict):
        """
        The next move on the game board
        :param action:
        :return:
        """
        assert self.action_space.contains(action)

        if action in self.already_played:
            rewards = self.rewards['already_played_last'] if action == self.last_played else self.rewards['already_played']

            return copy.deepcopy(self.game_board), rewards, False, {
                'points': self.points,
                'already_played': len(self.already_played),
                'num_errors': self.num_errors
            }

        if self.last_played is None:
            self.last_played = action
            self.game_board_copy = copy.deepcopy(self.game_board)
            self.game_board[action] = self.game_board_completed[action]
            self.already_played.append(action)

            return copy.deepcopy(self.game_board), self.rewards['first'], False, {
                'points': self.points,
                'already_played': len(self.already_played) - 1,
                'num_errors': self.num_errors
            }

        if self.game_board_completed[self.last_played] == self.game_board_completed[action]:
            self.points += 10
            self.game_board[action] = self.game_board_completed[action]
            self.already_played.append(action)
            self.last_played = None
            self.num_errors = 0
            self.correct += 1

            rewards = self.correct * self.rewards['correct']

            return copy.deepcopy(self.game_board), rewards, len(self.already_played) == self.nS, {
                'points': self.points,
                'already_played': len(self.already_played),
                'num_errors': self.num_errors
            }

        self.correct = 0

        self.num_errors += 1

        self.points = self.points - self.num_errors ** 2

        if self.points < 0:
            self.points = 0

        self.game_board[action] = self.game_board_completed[action]

        result_table = copy.deepcopy(self.game_board)

        self.game_board = copy.deepcopy(self.game_board_copy)
        self.game_board_copy = None

        if self.last_played in self.already_played:
            self.already_played.remove(self.last_played)

        self.last_played = None

        return result_table, self.rewards['wrong'], False, {
            'points': self.points,
            'already_played': len(self.already_played),
            'num_errors': self.num_errors
        }

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            return_info: bool = False,
            options: Optional[dict] = None,
    ):
        # super().reset(seed=seed)

        self.game_board_completed = []
        self.game_board = []
        self.game_board_copy = []
        self.already_played = []
        self.points = 0
        self.num_errors = 0
        self.last_played = None

        if self.r_game_board and self.r_game_board_completed:
            self.game_board_completed, self.game_board = self.r_game_board_completed, self.r_game_board
        else:
            self.game_board_completed, self.game_board = createGameBoard(self.shape[0], self.shape[1], 0)

        return copy.deepcopy(self.game_board)

    def render(self, game_board=None, mode='human'):
        outfile = StringIO()

        outfile.write(f'-- Memory Game - Points: {self.points} --\n')

        print_game_board = game_board if game_board is not None else self.game_board

        line = []
        for item in print_game_board:
            line.append(item)

            if len(line) == self.shape[0]:
                outfile.write('  '.join(map(str, line)))
                outfile.write('\n')
                line = []

        with closing(outfile):
            return outfile.getvalue()
