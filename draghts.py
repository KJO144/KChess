from TTT import Piece
from base import Board, Player
from enum import Enum

class DraughtsPiece(Enum):

    B = 0
    W = 1
    E = 2

    def __str__(self):
        return " " if self.name == 'E' else self.name
    
    def owner(self):
        owners = {'B': Player['B'], 'W': Player['W'], 'E': None}
        return owners[self.name]

def _initial_position():    
    pos = {}
    for i in range(8):
        for j in range(8):
            square = (i,j)# row, column
            
            if (i+j)%2 == 1 and i<=2:
                p = DraughtsPiece['W']
            elif (i+j)%2 == 1 and i>=5:
                p = DraughtsPiece['B']
            else:
                p = DraughtsPiece['E']
            pos[square] = p
    return pos
    
class DraughtsBoard(Board):

    def __init__(self, position=_initial_position(), player_to_move=Player['W']):
        self.player_to_move = player_to_move
        self.position = position
    
    _moves = {DraughtsPiece['W']: [(1,1), (1,-1)], DraughtsPiece['B']: [(-1,-1), (-1, 1)]}

    def legal_moves(self):
        """
        List of legal moves.
        A move is a triple of squares (from,to, del). Del is a DraughtsPiece that is taken.
        """
        
        pos = self.position
        player_to_move = self.player_to_move
        other_player = player_to_move.other_player()
        lm = []
        for from_sq, Piece in pos.items():
            if Piece.owner() == player_to_move:
                for (xm, ym) in self._moves[Piece]:
                    to_square = (from_sq[0] + xm, from_sq[1] + ym)
                    to_square_beyond = (to_square[0] + xm, to_square[1] + ym)
                    # regular move
                    if pos.get(to_square) == DraughtsPiece['E']:
                        lm.append((from_sq, to_square, None))
                    # capture
                    if pos.get(to_square) == DraughtsPiece[other_player.name] and (pos.get(to_square_beyond) == DraughtsPiece['E']):
                        lm.append((from_sq, to_square_beyond, to_square))
        return lm

    def num_pieces(self):
        pos = self.position
        W = len( [piece for sq, piece in pos.items() if piece.owner == Player['W']])
        B = len( [piece for sq, piece in pos.items() if piece.owner == Player['B']])
        return W,B

    def winner(self):
        nwhite, nblack = self.num_pieces()
        if nwhite == 0 and nblack != 0:
            return Player['B']
        elif nblack == 0 and nwhite != 0:
            return Player['W']
        else:
            return None

    def evaluation(self):
        nwhite, nblack = self.num_pieces()
        return (nwhite-nblack)-(nwhite+nblack)

    def game_over(self):
        return self.winner is not None

    def make_move(self, move):
        """
        Return a new board with the move played.
        """
        player_to_move = self.player_to_move
        from_square, to_square, empty_square = move
        assert(self.position[from_square].owner() == player_to_move)
                
        new_pos = self.position.copy()

        new_pos[from_square] = DraughtsPiece['E']
        new_pos[to_square] = DraughtsPiece[player_to_move.name]
        if empty_square is not None:
            assert(new_pos[empty_square].owner() == player_to_move.other_player())
            new_pos[empty_square] = DraughtsPiece['E']
        new_turn = player_to_move.other_player()
        return DraughtsBoard(new_pos, new_turn)

    def __str__(self):
        """Return a string representation of the board"""
        p = self.position.values()
        p = [str(x) for x in p]

        rows = [" ".join(p[0+i:8+i]) for i in range(0, 8*8, 8)]
        ret = "\n".join([f"[ {x} ]" for x in reversed(rows)])
        ret+= f" ({self.player_to_move})"
        return ret



def squid(move):
    """"""
    from_sq, to_sq, _  = move
    return (f"{chr(96+from_sq[1]+1)}{from_sq[0]+1}-{chr(96+to_sq[1]+1)}{to_sq[0]+1}")
    


b = DraughtsBoard()

move = ((2,1), (3,0), None)

nb = b.make_move(move)
print(nb, "\n")

lm = nb.legal_moves()

move2 = ((5,2), (4,1), None)
# move2 = tuple(squid(x) for x in move2)
nb2 = nb.make_move(move2)
print(nb2, "\n")

move3 = ((3,0), (5,2), (4,1))
nb3 = nb2.make_move(move3)
print(nb3, "\n")

lm = nb3.legal_moves()
print(lm)

lm =  [squid(move) for move in lm]
print(lm)

