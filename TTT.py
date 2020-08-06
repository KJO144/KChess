import numpy as np
from enum import Enum

def _wins():
    """Returns a list of lists representing winning positions"""
    a = np.array(range(9)).reshape((3,3))
    rows = [list(a[i,:]) for i in range(3)]
    cols = [list(a[:,i]) for i in range(3)]
    wins = rows + cols + [[0,4,8]] + [[2,4,6]]
    return(wins)
    
class Board():
    
    def __init__(self, position, turn):
        self.turn = turn
        self.position = position
        
    def legal_moves(self):
        """
        List of legal moves.
        A move is a tuple (square, piece).
        """
        piece_to_play = Piece[self.turn]
        return [(sq, piece_to_play) for sq,piece in self.position.items() if piece == Piece['E']]
                      
    def make_move(self, move):
        """
        Return a new board with move played.
        """
        square, piece = move
        new_pos = self.position.copy()
        new_pos[square] = piece
        new_turn = {'B':'W', 'W': 'B'}[self.turn]
        return Board(new_pos, new_turn)
    
    def __str__(self):
        p = self.position
        ret1 = f"[ {p[0]} {p[1]} {p[2]} ]"
        ret2 = f"[ {p[3]} {p[4]} {p[5]} ]"
        ret3 = f"[ {p[6]} {p[7]} {p[8]} ]"
        return ret1 + "\n" + ret2 + "\n" + ret3

    wins = _wins()

    def game_over(self):
        return self.winner() != 'N' or len(self.legal_moves()) == 0

    def winner(self):
        """Returns W if white has won, B if black as won, and N otherwise"""
        pos = self.position
        wins = self.wins

        for [w0, w1, w2] in wins:
            if pos[w0] == pos[w1]:
                if pos[w1] == pos[w2]:
                    if pos[w0] is not Piece['E']:
                        return pos[w0].name
        return 'N'

class Piece(Enum):
    
    B = 0
    W = 1
    E = 2
    def __str__(self):
        return self.name

def minimax(board, move):
    """Returns a score for move."""
    
    turn = board.turn
    new_board = board.make_move(move)
    
    winner = new_board.winner()
    
    if winner == 'W' and turn == 'W':
        return 1
    if winner == 'B' and turn == 'B':
        return -1

    assert(winner == 'N')
    legal_moves = new_board.legal_moves()
    
    if len(legal_moves) == 0:
        return(0)

    scores = [minimax(new_board, lm) for lm in legal_moves]
    
    if turn == 'W':
        ret = min(scores)
    if turn == 'B':
        ret = max(scores)

    return(ret)

def best_move(board):
    """
    Returns the best move on the board.
    """

    legal_moves = board.legal_moves()
    if len(legal_moves) == 0:
        return None
    scores = np.array([minimax(board, move) for move in legal_moves])
    if board.turn == 'W':
        index = scores.argmax()
    else:
        index = scores.argmin()

    return legal_moves[index]
