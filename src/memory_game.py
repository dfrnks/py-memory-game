import os
import copy
import time
import random
import logging


class MemoryGame:
    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
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
        self.game_table = [['000' for w in range(self.width)] for h in range(self.height)]

    def __getNewObj(self, el):
        obj = random.randint(100, 99 + el)

        self.used[obj] = 1 if obj not in self.used else self.used[obj] + 1

        if self.used[obj] > 2:
            return self.__getNewObj(el)

        return obj

    def __cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def __playing(self, message=None):
        self.print(message)

        position = input("Enter the el position (ex: 12):")

        if len(position) > 2 or len(position) < 2:
            self.__playing("Digit two numbers. Ex: 12")
            return

        w = int(position[0])
        h = int(position[1])

        if w == 0 or h == 0:
            self.__playing("Positions cannot be zero")
            return

        if w > self.width:
            self.__playing(f"First number cannot be greater than {self.width}")
            return

        if h > self.height:
            self.__playing(f"Second number cannot be greater than {self.height}")
            return

        h = h - 1
        w = w - 1

        if f'{w}{h}' in self.positions:
            self.__playing("Position already played")
            return

        r = self.result_table[h][w]
        if self.last is None:
            self.last = [h, w]
            self.game_table_copy = copy.deepcopy(self.game_table)
            self.game_table[h][w] = r
            self.positions.append(f'{w}{h}')
        elif self.result_table[self.last[0]][self.last[1]] == r:
            self.points += 10
            self.game_table[h][w] = r
            self.positions.append(f'{w}{h}')
            self.last = None
            self.num_errors = 0

            if len(self.positions) == (self.width * self.height):
                self.print()

                logging.info(f"Gaming complete, Total points: {self.points}")
                return
        else:
            self.num_errors += 1
            punicao = self.num_errors ** 2
            self.points = self.points - punicao if self.points - punicao >= 0 else 0
            self.game_table[h][w] = r
            self.print()
            self.game_table = copy.deepcopy(self.game_table_copy)
            self.game_table_copy = None

            if f'{self.last[1]}{self.last[0]}' in self.positions:
                self.positions.remove(f'{self.last[1]}{self.last[0]}')

            self.last = None

            time.sleep(1)

        self.__playing()

    def print(self, message=None):
        self.__cls()

        if message:
            logging.error(message)

        logging.info(f'-- Memory Game - Points: {self.points} --')
        for line in self.game_table:
            logging.info('  '.join(map(str, line)))

        time.sleep(0.1)

    def start(self):

        self.__createTable()

        # for line in self.result_table:
        #     print('  '.join(map(str, line)))

        self.__playing()
