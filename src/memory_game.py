import os
import copy
import time
import random
import logging


class MemoryGame:
    def __init__(self, width=4, height=4, character='*'):
        self.width = width
        self.height = height
        self.character = character * 3
        self.result_table = []
        self.game_table = []
        self.game_table_copy = None
        self.used = {}
        self.points = 0
        self.last = None
        self.positions = []
        self.num_errors = 0

    def __createTable(self):
        self.used = {}

        el = (self.width * self.height) / 2

        logging.debug(f'Elements number: {el}')

        if el % 2 != 0:
            raise Exception('Width and height is not a par number.')

        if el <= 2:
            raise Exception('The number of elements must be great than 2')

        self.result_table = [[self.__getNewObj(el) for w in range(self.width)] for h in range(self.height)]
        self.game_table = [[self.character for w in range(self.width)] for h in range(self.height)]

    def __getNewObj(self, el):
        obj = random.randint(100, 99 + el)

        self.used[obj] = 1 if obj not in self.used else self.used[obj] + 1

        if self.used[obj] > 2:
            return self.__getNewObj(el)

        return obj

    def __cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def playing(self, message=None):
        self.print(message)

        position = input("Enter the Width Height position (ex: 12):")

        if len(position) > 2 or len(position) < 2:
            self.playing("Digit two numbers. Ex: 12")
            return

        w = int(position[0]) - 1
        h = int(position[1]) - 1

        try:
            finished, table, points, right = self.next(width=w, height=h)

            if finished:
                self.print()

                logging.info(f"Gaming complete, Total points: {points}")

                return

        except Exception as err:
            self.playing(err)
            return

        if right == 0:
            self.print()
        elif right == 1:
            self.print()
        elif right == -1:
            self.print(table=table)
            time.sleep(1)
            self.print()
        elif right == -2:
            self.print("Position already played")

        self.playing()

    def print(self, message=None, table=None):
        self.__cls()

        if message:
            logging.error(message)

        logging.info(f'-- Memory Game - Points: {self.points} --')
        if table is None:
            for line in self.game_table:
                logging.info('  '.join(map(str, line)))
        else:
            for line in table:
                logging.info('  '.join(map(str, line)))

        time.sleep(0.1)

    def start(self):
        self.__createTable()

    def next(self, width: int, height: int) -> [bool, list, int, int]:
        if width > self.width - 1:
            raise Exception(f"Width number cannot be greater than {self.width}")

        if height > self.height - 1:
            raise Exception(f"Height number cannot be greater than {self.height}")

        if f'{width}{height}' in self.positions:
            return False, self.game_table, self.points, -2

        r = self.result_table[height][width]
        if self.last is None:
            self.last = [height, width]
            self.game_table_copy = copy.deepcopy(self.game_table)
            self.game_table[height][width] = r
            self.positions.append(f'{width}{height}')
            result_table = copy.deepcopy(self.game_table)

            return False, result_table, self.points, 0
        elif self.result_table[self.last[0]][self.last[1]] == r:
            self.points += 10
            self.game_table[height][width] = r
            self.positions.append(f'{width}{height}')
            self.last = None
            self.num_errors = 0

            result_table = copy.deepcopy(self.game_table)

            if len(self.positions) == (self.width * self.height):
                return True, result_table, self.points, 1

            return False, result_table, self.points, 1

        self.num_errors += 1
        penalty = self.num_errors ** 2
        self.points = self.points - penalty if self.points - penalty >= 0 else 0

        self.game_table[height][width] = r
        result_table = copy.deepcopy(self.game_table)
        self.game_table = copy.deepcopy(self.game_table_copy)
        self.game_table_copy = None

        if f'{self.last[1]}{self.last[0]}' in self.positions:
            self.positions.remove(f'{self.last[1]}{self.last[0]}')

        self.last = None

        return False, result_table, self.points, -1
