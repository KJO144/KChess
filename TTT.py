import numpy as np
from enum import Enum
from base import Board, Piece, Player

class TTTPiece(Piece, Enum):
    
    B = 0
    W = 1
    E = 2
    def __str__(self):
        return " " if self.name == 'E' else self.name
    
    def owner(self):
        owners = {'B': Player['B'], 'W': Player['W'], 'E': None}
        return owners[self.name]
    


def _wins():
    """Returns a list of lists representing winning positions"""
    a = np.array(range(9)).reshape((3,3))
    rows = [list(a[i,:]) for i in range(3)]
    cols = [list(a[:,i]) for i in range(3)]
    wins = rows + cols + [[0,4,8]] + [[2,4,6]]
    return(wins)

def _initial_position():
    return {i: TTTPiece['E'] for i in range(9)}

class TTTBoard(Board):
    
    def __init__(self, position = _initial_position(), player_to_move = Player['W']):
        self.player_to_move = player_to_move
        self.position = position
    
    def legal_moves(self):
        """
        List of legal moves.
        A move is a tuple (square, piece).
        """
        piece_to_play = TTTPiece[self.player_to_move.name]
        return [(sq, piece_to_play) for sq,piece in self.position.items() if piece == TTTPiece['E']]
                      
    def make_move(self, move):
        """
        Return a new board with move played.
        """
        square, piece = move
        new_pos = self.position.copy()
        new_pos[square] = piece
        new_turn = self.player_to_move.other_player()
        return TTTBoard(new_pos, new_turn)
    
    def __str__(self):
        p = self.position
        ret1 = f"[ {p[0]} {p[1]} {p[2]} ]"
        ret2 = f"[ {p[3]} {p[4]} {p[5]} ]"
        ret3 = f"[ {p[6]} {p[7]} {p[8]} ]"
        return ret1 + "\n" + ret2 + "\n" + ret3

    wins = _wins()

    def game_over(self):
        return self.winner() is not None or len(self.legal_moves()) == 0

    def winner(self):
        """If the position is a win returns the winner. Otherwise None."""
        pos = self.position
        wins = self.wins

        for [w0, w1, w2] in wins:
            if pos[w0] == pos[w1]:
                if pos[w1] == pos[w2]:
                    if pos[w0] is not TTTPiece['E']:
                        return pos[w0].owner()
        return None

