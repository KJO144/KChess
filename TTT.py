import numpy as np

class Board():
    
    def __init__(self, position, turn):
        self.turn = turn
        self.position = position
        
    def legal_moves(self):
        """a move is a tuple (square, piece)"""
        return [(sq, Piece(self.turn)) for sq,piece in self.position.items() if piece == Piece('E')]
              
    def make_move(self, move):
        square, piece = move
        new_pos = self.position.copy()
        new_pos[square] = piece
        new_turn = {'B':'W', 'W': 'B'}[self.turn]
        return Board(new_pos, new_turn)
    
    def __str__(self):
        ret = str([str(piece) for sq, piece in self.position.items()]) + f" ({self.turn})"
        return ret

    def winner(self):
        """Returns W if white has won, B if black as won, and N otherwise"""
        pos = self.position
        a = np.array(range(9)).reshape((3,3))
        rows = [list(a[i,:]) for i in range(3)]
        cols = [list(a[:,i]) for i in range(3)]
        wins = rows + cols + [[0,4,8]] + [[2,4,6]]

        for win in wins:    
            uniq = list(set([pos[i] for i in win]))
            if len(uniq) == 1 and uniq[0] != Piece('E'):
                return {Piece('W'): 'W', Piece('B'): 'B'}[uniq[0]]
        return 'N'

        
    
class Piece():
    
    def __init__(self, _type):
        self.type = _type # B (black), W (white) or E(empty)
    
    def __eq__(self, other):
        return self.type == other.type
    
    def __str__(self):
        return f"{self.type}"
    
    def __hash__(self):
        return({'B': 0, 'W': 1, 'E': 2}[self.type])
