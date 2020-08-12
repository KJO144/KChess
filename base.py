from abc import ABC
from enum import Enum

class Piece:

    pass

class Board(ABC):
    pass

class Player(Enum):
    B = 0
    W = 1

    def other_player(self):
        if self.name == 'B':
            return Player['W']
        elif self.name == 'W':
            return Player['B']

    def top_score(self):
        return {'B': -1, 'W': 1}[self.name]
    