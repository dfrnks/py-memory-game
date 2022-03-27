from contextlib import closing
from io import StringIO
import numpy as np
from gym import Env, spaces
from typing import Optional
import random
import copy


def createTable(width, height, character):
    el = (width * height) / 2

    # logging.debug(f'Elements number: {el}')

    if el % 2 != 0:
        raise Exception('Width and height is not a par number.')

    if el <= 2:
        raise Exception('The number of elements must be great than 2')

    used = {}

    def getNewObj(e):
        obj = random.randint(100, 99 + e)

        used[obj] = 1 if obj not in used else used[obj] + 1

        if used[obj] > 2:
            return getNewObj(e)

        return obj

    result_table = [getNewObj(el) for w in range(width * height)]
    game_table = [character for w in range(width * height)]

    return result_table, game_table


class MemoryGameEnv(Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, shape=(8, 8)):
        self.shape = shape

        self.nS = np.prod(self.shape)

        # Set this in SOME subclasses
        self.reward_range = (-float("inf"), float("inf"))

        # Set these in ALL subclasses
        self.observation_space = spaces.Discrete(self.nS)
        self.action_space = spaces.Discrete(self.nS)

        self.result_table = []
        self.game_table = []
        self.game_table_copy = []
        self.already_take = []
        self.points = 0
        self.num_errors = 0
        self.last = None

    def step(self, action):
        assert self.action_space.contains(action)

        if action in self.already_take:
            return self.game_table, 0, False, {'points': self.points}

        if self.last is None:
            self.last = action
            self.game_table_copy = copy.deepcopy(self.game_table)
            self.game_table[action] = self.result_table[action]
            self.already_take.append(action)

            return self.game_table, 0, False, {'points': self.points}

        if self.result_table[self.last] == self.result_table[action]:
            self.points += 10
            self.game_table[action] = self.result_table[action]
            self.already_take.append(action)
            self.last = None
            self.num_errors = 0

            if len(self.already_take) == self.nS:
                return self.game_table, 10, True, {'points': self.points}

            return self.game_table, 10, False, {'points': self.points}

        self.num_errors += 1

        penalty = self.num_errors ** 2
        self.points = self.points - penalty

        if self.points < 0:
            self.points = 0

        self.game_table[action] = self.result_table[action]

        result_table = copy.deepcopy(self.game_table)

        self.game_table = copy.deepcopy(self.game_table_copy)
        self.game_table_copy = None

        if self.last in self.already_take:
            self.already_take.remove(self.last)

        self.last = None

        return result_table, - 10, False, {'points': self.points}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)

        self.result_table = []
        self.game_table = []
        self.game_table_copy = []
        self.already_take = []
        self.points = 0
        self.num_errors = 0
        self.last = None

        self.result_table, self.game_table = createTable(self.shape[0], self.shape[1], 0)

        return self.game_table

    def render(self, table=None, mode="human"):
        outfile = StringIO()

        outfile.write(f'-- Memory Game - Points: {self.points} --\n')
        line = []
        if table is not None:
            for item in table:
                line.append(item)

                if len(line) == self.shape[0]:
                    outfile.write('  '.join(map(str, line)))
                    outfile.write("\n")
                    line = []
        else:
            for item in self.game_table:
                line.append(item)

                if len(line) == self.shape[0]:
                    outfile.write('  '.join(map(str, line)))
                    outfile.write("\n")
                    line = []

        with closing(outfile):
            return outfile.getvalue()
