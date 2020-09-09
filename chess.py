from base import Board, Player
from enum import Enum
from collections import defaultdict

class ChessPiece(Enum):

    WK = ('W', 7, 999, "King")
    WQ = ('W', 7, 9, "Queen")
    WB = ('W', 7, 3, "Bishop")
    WN = ('W', 7, 3, "Knight")
    WR = ('W', 7, 5, "Rook")
    WP = ('W', 7, 1, "Pawn")

    BK = ('B', 0, 999, "King")
    BQ = ('B', 0, 9, "Queen")
    BB = ('B', 0, 3, "Bishop")
    BN = ('B', 0, 3, "Knight")
    BR = ('B', 0, 5, "Rook")
    BP = ('B', 0, 1, "Pawn")

    E = (None, None, None, None)

    def __init__(self, owner_name, promotion_rank, gvalue, type):
        self.owner_name = owner_name
        self.promotion_rank = promotion_rank
        self.gvalue = gvalue
        self.type = type

    def owner(self):
        if self.owner_name:
            return Player[self.owner_name]
        else:
            return None

    def promotes_to(self):
        """What does this piece promote to when it hits the back rank"""
        vals = {'WP': ChessPiece['WQ'], 'BP': ChessPiece['BQ']}
        return vals.get( self.name, self.name)
        
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

    instreams = [ 'player_to_move', 'position', 'can_castle']

    _diag_movers = [ChessPiece['WQ'], ChessPiece['BQ'], ChessPiece['WB'], ChessPiece['BB']]
    _straight_movers = [ChessPiece['WQ'], ChessPiece['BQ'], ChessPiece['WR'], ChessPiece['BR']]
    _knights = [ChessPiece['WN'], ChessPiece['BN']]
    _kings = [ChessPiece['WK'], ChessPiece['BK']]

    def __init__(self, position=_initial_position(), player_to_move=Player['W'], can_castle={'WQS': True, 'BQS': True, 'WKS': True, 'BKS': True}):
        self.player_to_move = player_to_move
        self.position = position
        self.can_castle = can_castle

    def _moves(self, player_to_move):
        
        pos = self.position

        moves = []
                
        relevant_pieces = {sq: piece for sq, piece in pos.items() if piece.owner() == player_to_move}
        
        for from_sq, piece in relevant_pieces.items():
            if piece == ChessPiece['WP']:
                moves += _moves_for_direction(pos, from_sq, 1, (1,0), include_captures=False)
                moves += _moves_for_direction(pos, from_sq, 1, (1,1), only_captures=True)
                moves += _moves_for_direction(pos, from_sq, 1, (1,-1), only_captures=True)
                if from_sq[0] == 1:
                    moves += _moves_for_direction(pos, from_sq, 1, (2,0), include_captures=False)
                continue

            if piece == ChessPiece['BP']:
                moves += _moves_for_direction(pos, from_sq, 1, (-1,0), include_captures=False)
                moves += _moves_for_direction(pos, from_sq, 1, (-1,1), only_captures=True)
                moves += _moves_for_direction(pos, from_sq, 1, (-1,-1), only_captures=True)
                if from_sq[0] == 6:
                    moves += _moves_for_direction(pos, from_sq, 1, (-2,0), include_captures=False)
                continue
            
            if piece in self._diag_movers:
                moves += _moves_for_direction(pos, from_sq, 7, (1,1))
                moves += _moves_for_direction(pos, from_sq, 7, (1,-1))
                moves += _moves_for_direction(pos, from_sq, 7, (-1,-1))
                moves += _moves_for_direction(pos, from_sq, 7, (-1,1))
            
            if piece in self._straight_movers:
                moves += _moves_for_direction(pos, from_sq, 7, (1,0))
                moves += _moves_for_direction(pos, from_sq, 7, (-1,0))
                moves += _moves_for_direction(pos, from_sq, 7, (0,1))
                moves += _moves_for_direction(pos, from_sq, 7, (0,-1))

            if piece in self._knights:
                moves += _moves_for_direction(pos, from_sq, 1, (2,1))
                moves += _moves_for_direction(pos, from_sq, 1, (2,-1))
                moves += _moves_for_direction(pos, from_sq, 1, (-2,1))
                moves += _moves_for_direction(pos, from_sq, 1, (-2,-1))

                moves += _moves_for_direction(pos, from_sq, 1, (1,2))
                moves += _moves_for_direction(pos, from_sq, 1, (1,-2))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,-2))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,2))
                continue

            if piece in self._kings:
                moves += _moves_for_direction(pos, from_sq, 1, (1,1))
                moves += _moves_for_direction(pos, from_sq, 1, (1,-1))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,-1))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,1))
                moves += _moves_for_direction(pos, from_sq, 1, (1,0))
                moves += _moves_for_direction(pos, from_sq, 1, (-1,0))
                moves += _moves_for_direction(pos, from_sq, 1, (0,1))
                moves += _moves_for_direction(pos, from_sq, 1, (0,-1))
                if piece == ChessPiece['WK']:
                    if self.can_castle['WKS'] and from_sq == (0,4) and pos[(0,5)] == ChessPiece['E'] and pos[(0,6)] == ChessPiece['E'] and pos[(0,7)] == ChessPiece['WR']:
                        castling = ((0,4), (0,6))
                        moves.append(castling)
                    if self.can_castle['WQS'] and from_sq == (0,4) and pos[(0,3)] == ChessPiece['E'] and pos[(0,2)] == ChessPiece['E'] and pos[(0,1)] == ChessPiece['E'] and pos[(0,0)] == ChessPiece['WR']:
                        castling = ((0,4), (0,2))
                        moves.append(castling)
                if piece == ChessPiece['BK']:
                    if self.can_castle['BKS'] and from_sq == (7,4) and pos[(7,5)] == ChessPiece['E'] and pos[(7,6)] == ChessPiece['E'] and pos[(7,7)] == ChessPiece['BR']:
                        castling = ((7,4), (7,6))
                        moves.append(castling)
                    if self.can_castle['BQS'] and from_sq == (7,4) and pos[(7,3)] == ChessPiece['E'] and pos[(7,2)] == ChessPiece['E'] and pos[(7,1)] == ChessPiece['E'] and pos[(7,0)] == ChessPiece['BR']:
                        castling = ((7,4), (7,2))
                        moves.append(castling)


        return moves

    def _puts_me_in_check(self, move):
        """
        If move is made am I then in check?
        I will be in check if my opponent has a move that can capture my king.
        """
        new_board = self.make_move(move)
        moves = new_board._moves(new_board.player_to_move)

        my_king_pos = [sq for sq, piece in new_board.position.items() if piece == ChessPiece[self.player_to_move.name + 'K']]
        assert(len(my_king_pos)==1)
        my_king_pos = my_king_pos[0]
        king_captures = [m for m in moves if m[1] == my_king_pos]
        
        return len(king_captures) > 0

    def legal_moves(self):
        """
        List of legal moves.
        A move is a pair of squares (from,to).
        """
        
        # first list all the moves our pieces can make
        player_to_move = self.player_to_move
        moves =  self._moves(player_to_move)

        legal_moves = [ m for m in moves if not self._puts_me_in_check(m)]

        return legal_moves

    def _num_pieces(self):
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
        counts = self._num_pieces()
        del counts[ChessPiece['E']]
        sums = defaultdict(int)

        for piece, count in counts.items():
            sums[piece.owner()] += count * piece.gvalue
        W = sums[Player['W']]
        B = sums[Player['B']]
        return (W-B)/(W+B)

    def make_move(self, move):
        """
        Return a new board with the move played.
        """
        player_to_move = self.player_to_move
        from_square, to_square = move

        new_pos = self.position.copy()
                 
        moving_piece = new_pos[from_square]
        assert(moving_piece.owner() == player_to_move)

        is_promotion = (to_square[0] == moving_piece.promotion_rank)

        landing_piece = moving_piece if not is_promotion else moving_piece.promotes_to()
     
        new_pos[to_square] = landing_piece
        new_pos[from_square] = ChessPiece['E']
        
        if moving_piece == ChessPiece['WK'] and to_square == (0,6) and from_square == (0,4):
            new_pos[(0,7)] = ChessPiece['E']
            new_pos[(0,5)] = ChessPiece['WR']
        
        if moving_piece == ChessPiece['WK'] and to_square == (0,2) and from_square == (0,4):
            new_pos[(0,0)] = ChessPiece['E']
            new_pos[(0,3)] = ChessPiece['WR']

        if moving_piece == ChessPiece['BK'] and to_square == (7,6) and from_square == (7,4):
            new_pos[(7,7)] = ChessPiece['E']
            new_pos[(7,5)] = ChessPiece['BR']
        
        if moving_piece == ChessPiece['BK'] and to_square == (7,2) and from_square == (7,4):
            new_pos[(7,0)] = ChessPiece['E']
            new_pos[(7,3)] = ChessPiece['BR']


        can_castle = self.can_castle.copy()

        if moving_piece == ChessPiece['WK']:
            can_castle['WKS'] = False
            can_castle['WQS'] = False

        if moving_piece == ChessPiece['BK']:
            can_castle['BKS'] = False
            can_castle['BQS'] = False

        new_turn = player_to_move.other_player()
        return ChessBoard(new_pos, new_turn, can_castle)

    def __str__(self):
        """Return a string representation of the board"""
        p = self.position.values()
        p = [str(x) for x in p]

        rows = [" ".join(p[0+i:8+i]) for i in range(0, 8*8, 8)]
        ret = "\n".join([f"[ {x} ]" for x in reversed(rows)])
        evaluation = self.evaluation()
        cannot_castle = [side for side, value in self.can_castle.items() if value is False]
        ret += f" ({self.player_to_move}) ({evaluation}) ({cannot_castle})"
        return ret

def squid(move):
    """"""
    from_sq, to_sq = move
    return (f"{chr(96+from_sq[1]+1)}{from_sq[0]+1}-{chr(96+to_sq[1]+1)}{to_sq[0]+1}")
