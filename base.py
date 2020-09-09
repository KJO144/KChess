from abc import ABC
from enum import Enum
import json

class Piece:
    pass

class Board(ABC):

    instreams = None
    position = None
    player_to_move = None

    def winner(self):
        raise NotImplementedError

    def legal_moves(self):
        raise NotImplementedError

    def make_move(self, move):
        raise NotImplementedError

    def evaluation(self):
        raise NotImplementedError

    @classmethod
    def from_dict(cls, values):
        r = {name: value for name, value in values.items() if name in cls.instreams}
        return cls(**r)
    
    def to_json(self):
        winner = self.winner()

        ret = self.__dict__
        ret['player_to_move'] = ret['player_to_move'].name
        ret['position'] = {f"S{square[0]}{square[1]}": piece.name for square, piece in ret['position'].items() }
        if winner is not None:
            ret['winner'] = winner
        ret = json.dumps(ret)
        return ret        



class Player(Enum):
    B = (-1, 'W')
    W = (1, 'B')

    def __init__(self, top_score, other_player_name):
        self.top_score = top_score
        self.other_player_name = other_player_name

    def other_player(self):
        return Player[self.other_player_name]

