from base import Board, Player
from enum import Enum
from collections import defaultdict

class ChessPiece(Enum):

    WK = 0
    WQ = 1
    WB = 2
    WN = 3
    WR = 4
    WP = 5

    BK = 6
    BQ = 7
    BB = 8
    BN = 9
    BR = 10
    BP = 11

    E = 12

    def owner(self):
        L = self.name[0]
        ret = L if L=='E' else Player[L]
        return ret

    def promotes_to(self):
        """What does this piece promote to when it hits the back rank"""
        vals = {'WP': ChessPiece['WQ'], 'BP': ChessPiece['BQ']}
        return vals.get( self.name, self.name)
        
    def promotion_rank(self):
        """Which row does this piece need to get to to promote"""
        vals = {'BP': 0, 'WP': 7}
        return vals.get( self.name, None)

    def value(self):
        values = {'K': 999, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
        T = self.name[1]
        return values[T]

    def __str__(self):
        ret = "E " if self.name == "E" else self.name
        return ret
    

def _initial_position():
    pos = {}
    for i in range(8):
        for j in range(8):
            pos[(i,j)] = ChessPiece['E']

    pos[(0,0)] = ChessPiece['WR']
    pos[(0,1)] = ChessPiece['WN']
    pos[(0,2)] = ChessPiece['WB']
    pos[(0,3)] = ChessPiece['WQ']
    pos[(0,4)] = ChessPiece['WK']
    pos[(0,5)] = ChessPiece['WB']
    pos[(0,6)] = ChessPiece['WN']
    pos[(0,7)] = ChessPiece['WR']

    pos[(7,0)] = ChessPiece['BR']
    pos[(7,1)] = ChessPiece['BN']
    pos[(7,2)] = ChessPiece['BB']
    pos[(7,3)] = ChessPiece['BQ']
    pos[(7,4)] = ChessPiece['BK']
    pos[(7,5)] = ChessPiece['BB']
    pos[(7,6)] = ChessPiece['BN']
    pos[(7,7)] = ChessPiece['BR']

    for i in range(8):
        pos[(1,i)] = ChessPiece['WP']
        pos[(6,i)] = ChessPiece['BP']
    return pos


def _offset_square(square, offset):
    return (square[0]+offset[0], square[1]+offset[1])



def _moves_for_direction(pos, start_square, max_distance, direction, include_captures=True, only_captures=False):
    end_squares = []
    piece = pos[start_square]
    tomove = piece.owner()
    
    for i in range(1, max_distance+1):
        offset = (direction[0]*i, direction[1]*i)
        sq = _offset_square(start_square, offset)
        if sq[0] < 0 or sq[0] > 7 or sq[1] < 0 or sq[1] > 7:
            break
        owner = pos[sq].owner()
        if owner == tomove:
            break
        
        if owner == tomove.other_player():
            if include_captures:
                end_squares.append(sq)
            break
        
        if not only_captures:
            end_squares.append(sq)
        
    return [(start_square, end_square) for end_square in end_squares]


class ChessBoard(Board):

    def __init__(self, position=_initial_position(), player_to_move=Player['W']):
        self.player_to_move = player_to_move
        self.position = position
        self.can_castle = {'WQS': True, 'BQS': True, 'WKS': True, 'BKS': True}

    
    # def _square_is_attacked  square):
    #     ppos, os = position
    #     plpos, ayer_to_move = player_to_move

    #pos,      opposition_pieces = {sq: piece for sq, piece in pos.items() if piece.owner() == player_to_move.other_player()}


        
    #     return False

    def legal_moves(self):
        """
        List of legal moves.
        A move is a pair of squares (from,to).
        """
        pos = self.position
        player_to_move = self.player_to_move

        moves = []
        
        diag_movers = [ChessPiece['WQ'], ChessPiece['BQ'], ChessPiece['WB'], ChessPiece['BB']]
        straight_movers = [ChessPiece['WQ'], ChessPiece['BQ'], ChessPiece['WR'], ChessPiece['BR']]
        knights = [ChessPiece['WN'], ChessPiece['BN']]
        kings = [ChessPiece['WK'], ChessPiece['BK']]
        
        relevant_pieces = {sq: piece for sq, piece in pos.items() if piece.owner() == player_to_move}
        
        for from_sq, piece in relevant_pieces.items():
            if piece == ChessPiece['WP']:
                moves += _moves_for_direction(pos, from_sq, 1, (1,0), include_captures=False)
                moves += _moves_for_direction(pos, from_sq, 1, (1,1), only_captures=True)
                moves += _moves_for_direction(pos, from_sq, 1, (1,-1), only_captures=True)
                if from_sq[0] == 1:
                    moves += _moves_for_direction(pos, from_sq, 1, (2,0), include_captures=False)
                
            if piece == ChessPiece['BP']:
                moves += _moves_for_direction(pos, from_sq, 1, (-1,0), include_captures=False)
                moves += _moves_for_direction(pos, from_sq, 1, (-1,1), only_captures=True)
                moves += _moves_for_direction(pos, from_sq, 1, (-1,-1), only_captures=True)
                if from_sq[0] == 6:
                    moves += _moves_for_direction(pos, from_sq, 1, (-2,0), include_captures=False)
            
            if piece in diag_movers:
                moves += _moves_for_direction(pos, from_sq, 7, (1,1))
                moves += _moves_for_direction(pos, from_sq, 7, (1,-1))
                moves += _moves_for_direction(pos, from_sq, 7, (-1,-1))
                moves += _moves_for_direction(pos, from_sq, 7, (-1,1))
            
            if piece in straight_movers:
                moves += _moves_for_direction(pos, from_sq, 7, (1,0))
                moves += _moves_for_direction(pos, from_sq, 7, (-1,0))
                moves += _moves_for_direction(pos, from_sq, 7, (0,1))
                moves += _moves_for_direction(pos, from_sq, 7, (0,-1))

            if piece in knights:
                moves += _moves_for_direction(pos, from_sq, 1, (2,1))
                moves += _moves_for_direction(pos, from_sq, 1, (2,-1))
                moves += _moves_for_direction(pos, from_sq, 1, (-2,1))
                moves += _moves_for_direction(pos, from_sq, 1, (-2,-1))

                moves += _moves_for_direction(pos, from_sq, 1, (1,2))
                moves += _moves_for_direction(pos, from_sq, 1, (1,-2))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,-2))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,2))

            if piece in kings:
                moves += _moves_for_direction(pos, from_sq, 1, (1,1))
                moves += _moves_for_direction(pos, from_sq, 1, (1,-1))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,-1))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,1))
                moves += _moves_for_direction(pos, from_sq, 1, (1,0))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,0))
                moves += _moves_for_direction(pos, from_sq, 1, (0,1))
                moves += _moves_for_direction(pos, from_sq, 1, (0,-1))

                # if from_sq == (0,4) and can_castle['WKS'] andpos,  pos[(0,5)] == ChessPiece['E'] and pos[(0,6)] == ChessPiece['E']:
                #     moves += [(0,4), (0,6)]
                # if can_castle['WQS'] andpos,  pos[(0,3)] == ChessPiece['E'] and pos[(0,2)] == ChessPiece['E'] and pos[(0,1)] == ChessPiece['E']:
                #     moves += [(0,4), (0,2)]



        return moves

    def num_pieces(self):
        """Returns pos, a dict mapping each piece to the counts of that piece on the board"""
        pos = self.position
        counts = defaultdict(int)
        for piece in pos.values():
            counts[piece] += 1
        return counts

    def winner(self):
        """
        There is a winner if one side has no pieces.
        """
        return None

    def evaluation(self):
        """
        Returns a float representing the evaluation of the board position.
        Positive/negative if white/black has an advantage.
        """
        counts = self.num_pieces()
        del counts[ChessPiece['E']]
        sums = defaultdict(int)

        for piece, count in counts.items():
            sums[piece.owner()] += count * piece.value()
        W = sums[Player['W']]
        B = sums[Player['B']]
        return (W-B)/(W+B)

    def game_over(self):
        """
        The game is over if there is a winner.
        """
        return self.winner() is not None

    def make_move(self, move):
        """
        Return a new board with the move played.
        """
        player_to_move = self.player_to_move
        from_square, to_square = move

        new_pos = self.position.copy()
                 
        moving_piece = new_pos[from_square]
        assert(moving_piece.owner() == player_to_move)

        is_promotion = (to_square[0] == moving_piece.promotion_rank())

        landing_piece = moving_piece if not is_promotion else moving_piece.promotes_to()
     
        new_pos[to_square] = landing_piece
        new_pos[from_square] = ChessPiece['E']
        # if can_castle['WKS'] andpos,  moving_piece == ChessPiece['WK'] and to_square[1] == 6 and from_square[1] == 4:
        #     new_pos[(0,7)] = ChessPiece['E']
        #     new_pos[(0,5)] = ChessPiece['WR']
        #     can_castle['WKS'] = Fpos, alse
           
        

        new_turn = player_to_move.other_player()
        return ChessBoard(new_pos, new_turn)

    def __str__(self):
        """Return a string representation of the board"""
        p = self.position.values()
        p = [str(x) for x in p]

        rows = [" ".join(p[0+i:8+i]) for i in range(0, 8*8, 8)]
        ret = "\n".join([f"[ {x} ]" for x in reversed(rows)])
        evaluation = self.evaluation()
        ret += f" ({self.player_to_move}) ({evaluation})"
        return ret

def squid(move):
    """"""
    from_sq, to_sq = move
    return (f"{chr(96+from_sq[1]+1)}{from_sq[0]+1}-{chr(96+to_sq[1]+1)}{to_sq[0]+1}")

# b = ChessBoard()
# print(b)
# print("\n")

# for i in range(10):
#     lm = b.legal_moves()
#     move = lm[0]
#     b = b.make_move(move)
#     print(squid(move))
#     print(b)
#     print("\n\n")
