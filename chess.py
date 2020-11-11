from base import Board, Player
from enum import Enum
from collections import defaultdict


class ChessPiece(Enum):

    WK = (Player['W'], 7, 999, "King")
    WQ = (Player['W'], 7, 9, "Queen")
    WB = (Player['W'], 7, 3, "Bishop")
    WN = (Player['W'], 7, 3, "Knight")
    WR = (Player['W'], 7, 5, "Rook")
    WP = (Player['W'], 7, 1, "Pawn")

    BK = (Player['B'], 0, 999, "King")
    BQ = (Player['B'], 0, 9, "Queen")
    BB = (Player['B'], 0, 3, "Bishop")
    BN = (Player['B'], 0, 3, "Knight")
    BR = (Player['B'], 0, 5, "Rook")
    BP = (Player['B'], 0, 1, "Pawn")

    E = (None, None, None, None)

    def __init__(self, owner, promotion_rank, gvalue, type):
        self.owner = owner
        self.promotion_rank = promotion_rank
        self.gvalue = gvalue
        self.type = type

    def promotes_to(self):
        """What does this piece promote to when it hits the back rank"""
        vals = {'WP': ChessPiece['WQ'], 'BP': ChessPiece['BQ']}
        return vals.get(self.name, self)

    def __str__(self):
        ret = "E " if self.name == "E" else self.name
        return ret


def blank_board(piece=ChessPiece['E']):
    pos = {}
    for i in range(8):
        for j in range(8):
            pos[(i, j)] = piece
    return pos


def _initial_position():
    pos = blank_board()

    pos[(0, 0)] = ChessPiece['WR']
    pos[(0, 1)] = ChessPiece['WN']
    pos[(0, 2)] = ChessPiece['WB']
    pos[(0, 3)] = ChessPiece['WQ']
    pos[(0, 4)] = ChessPiece['WK']
    pos[(0, 5)] = ChessPiece['WB']
    pos[(0, 6)] = ChessPiece['WN']
    pos[(0, 7)] = ChessPiece['WR']

    pos[(7, 0)] = ChessPiece['BR']
    pos[(7, 1)] = ChessPiece['BN']
    pos[(7, 2)] = ChessPiece['BB']
    pos[(7, 3)] = ChessPiece['BQ']
    pos[(7, 4)] = ChessPiece['BK']
    pos[(7, 5)] = ChessPiece['BB']
    pos[(7, 6)] = ChessPiece['BN']
    pos[(7, 7)] = ChessPiece['BR']

    for i in range(8):
        pos[(1, i)] = ChessPiece['WP']
        pos[(6, i)] = ChessPiece['BP']

    can_castle = {'WQS': True, 'BQS': True, 'WKS': True, 'BKS': True}
    position = {'position': pos, 'player_to_move': Player['W'], 'can_castle': can_castle, 'history': []}
    position['previous_move'] = "none"
    return position


def _offset_square(square, offset):
    return (square[0]+offset[0], square[1]+offset[1])


def _moves_for_direction(pos, start_square, max_distance, direction, include_captures=True, only_captures=False):
    end_squares = []
    piece = pos[start_square]
    tomove = piece.owner

    for i in range(1, max_distance+1):
        offset = (direction[0]*i, direction[1]*i)
        sq = _offset_square(start_square, offset)
        if sq[0] < 0 or sq[0] > 7 or sq[1] < 0 or sq[1] > 7:
            break
        owner = pos[sq].owner
        if owner is tomove:
            break

        if owner is tomove.other_player():
            if include_captures:
                end_squares.append(sq)
            break

        if not only_captures:
            end_squares.append(sq)

    return [(start_square, end_square) for end_square in end_squares]


class ChessBoard(Board):

    instreams = ['player_to_move', 'position', 'can_castle', 'previous_move']

    _diag_movers = [ChessPiece['WQ'], ChessPiece['BQ'], ChessPiece['WB'], ChessPiece['BB']]
    _straight_movers = [ChessPiece['WQ'], ChessPiece['BQ'], ChessPiece['WR'], ChessPiece['BR']]
    _knights = [ChessPiece['WN'], ChessPiece['BN']]
    _kings = [ChessPiece['WK'], ChessPiece['BK']]

    def __init__(self, **kwargs):
        if kwargs == {}:
            kwargs = _initial_position()

        for name, value in kwargs.items():
            setattr(self, name, value)

    def _moves(self, player_to_move):

        pos = self.position

        WR = ChessPiece['WR']
        BR = ChessPiece['BR']

        a1 = (0, 0)
        b1 = (0, 1)
        c1 = (0, 2)
        d1 = (0, 3)
        e1 = (0, 4)
        f1 = (0, 5)
        g1 = (0, 6)
        h1 = (0, 7)

        a8 = (7, 0)
        b8 = (7, 1)
        c8 = (7, 2)
        d8 = (7, 3)
        e8 = (7, 4)
        f8 = (7, 5)
        g8 = (7, 6)
        h8 = (7, 7)

        moves = []
        E = ChessPiece['E']

        relevant_pieces = {sq: piece for sq, piece in pos.items() if piece.owner == player_to_move}

        for from_sq, piece in relevant_pieces.items():
            if piece == ChessPiece['WP']:
                moves += _moves_for_direction(pos, from_sq, 1, (1, 0), include_captures=False)
                moves += _moves_for_direction(pos, from_sq, 1, (1, 1), only_captures=True)
                moves += _moves_for_direction(pos, from_sq, 1, (1, -1), only_captures=True)
                if from_sq[0] == 1:
                    moves += _moves_for_direction(pos, from_sq, 1, (2, 0), include_captures=False)
                continue

            if piece == ChessPiece['BP']:
                moves += _moves_for_direction(pos, from_sq, 1, (-1, 0), include_captures=False)
                moves += _moves_for_direction(pos, from_sq, 1, (-1, 1), only_captures=True)
                moves += _moves_for_direction(pos, from_sq, 1, (-1, -1), only_captures=True)
                if from_sq[0] == 6:
                    moves += _moves_for_direction(pos, from_sq, 1, (-2, 0), include_captures=False)
                continue

            if piece in self._diag_movers:
                moves += _moves_for_direction(pos, from_sq, 7, (1, 1))
                moves += _moves_for_direction(pos, from_sq, 7, (1, -1))
                moves += _moves_for_direction(pos, from_sq, 7, (-1, -1))
                moves += _moves_for_direction(pos, from_sq, 7, (-1, 1))

            if piece in self._straight_movers:
                moves += _moves_for_direction(pos, from_sq, 7, (1, 0))
                moves += _moves_for_direction(pos, from_sq, 7, (-1, 0))
                moves += _moves_for_direction(pos, from_sq, 7, (0, 1))
                moves += _moves_for_direction(pos, from_sq, 7, (0, -1))

            if piece in self._knights:
                moves += _moves_for_direction(pos, from_sq, 1, (2, 1))
                moves += _moves_for_direction(pos, from_sq, 1, (2, -1))
                moves += _moves_for_direction(pos, from_sq, 1, (-2, 1))
                moves += _moves_for_direction(pos, from_sq, 1, (-2, -1))

                moves += _moves_for_direction(pos, from_sq, 1, (1, 2))
                moves += _moves_for_direction(pos, from_sq, 1, (1, -2))
                moves += _moves_for_direction(pos, from_sq, 1, (-1, -2))
                moves += _moves_for_direction(pos, from_sq, 1, (-1, 2))
                continue

            if piece in self._kings:
                moves += _moves_for_direction(pos, from_sq, 1, (1, 1))
                moves += _moves_for_direction(pos, from_sq, 1, (1, -1))
                moves += _moves_for_direction(pos, from_sq, 1, (-1, -1))
                moves += _moves_for_direction(pos, from_sq, 1, (-1, 1))
                moves += _moves_for_direction(pos, from_sq, 1, (1, 0))
                moves += _moves_for_direction(pos, from_sq, 1, (-1, 0))
                moves += _moves_for_direction(pos, from_sq, 1, (0, 1))
                moves += _moves_for_direction(pos, from_sq, 1, (0, -1))
                if piece == ChessPiece['WK'] and from_sq == e1:
                    if self.can_castle['WKS'] and pos[f1] == E and pos[g1] == E and pos[h1] == WR:
                        moves.append((e1, g1))
                    if self.can_castle['WQS'] and pos[d1] == E and pos[c1] == E and pos[b1] == E and pos[a1] == WR:
                        moves.append((e1, c1))
                if piece == ChessPiece['BK'] and from_sq == e8:
                    if self.can_castle['BKS'] and pos[f8] == E and pos[g8] == E and pos[h8] == BR:
                        moves.append((e8, g8))
                    if self.can_castle['BQS'] and pos[d8] == E and pos[c8] == E and pos[b8] == E and pos[a8] == BR:
                        moves.append((e8, c8))

        return moves

    def _puts_me_in_check(self, move):
        """
        If move is made am I then in check?
        I will be in check if my opponent has a move that can capture my king.
        """
        new_board = self.make_move(move)
        moves = new_board._moves(new_board.player_to_move)

        my_king = ChessPiece[self.player_to_move.name + 'K']
        my_king_pos = [sq for sq, piece in new_board.position.items() if piece == my_king]
        assert(len(my_king_pos) == 1)
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
        moves = self._moves(player_to_move)

        legal_moves = [m for m in moves if not self._puts_me_in_check(m)]

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
            sums[piece.owner] += count * piece.gvalue
        W = sums[Player['W']]
        B = sums[Player['B']]

        piece_value = (W-B)

        return piece_value

    def make_move(self, move):
        """
        Return a new board with the move played.
        """
        player_to_move = self.player_to_move
        from_square, to_square = move

        new_pos = self.position.copy()

        moving_piece = new_pos[from_square]
        assert(moving_piece.owner == player_to_move)

        is_promotion = (to_square[0] == moving_piece.promotion_rank)

        landing_piece = moving_piece if not is_promotion else moving_piece.promotes_to()

        new_pos[to_square] = landing_piece
        new_pos[from_square] = ChessPiece['E']

        if moving_piece == ChessPiece['WK'] and to_square == (0, 6) and from_square == (0, 4):
            new_pos[(0, 7)] = ChessPiece['E']
            new_pos[(0, 5)] = ChessPiece['WR']

        if moving_piece == ChessPiece['WK'] and to_square == (0, 2) and from_square == (0, 4):
            new_pos[(0, 0)] = ChessPiece['E']
            new_pos[(0, 3)] = ChessPiece['WR']

        if moving_piece == ChessPiece['BK'] and to_square == (7, 6) and from_square == (7, 4):
            new_pos[(7, 7)] = ChessPiece['E']
            new_pos[(7, 5)] = ChessPiece['BR']

        if moving_piece == ChessPiece['BK'] and to_square == (7, 2) and from_square == (7, 4):
            new_pos[(7, 0)] = ChessPiece['E']
            new_pos[(7, 3)] = ChessPiece['BR']

        can_castle = self.can_castle.copy()

        if moving_piece == ChessPiece['WK']:
            can_castle['WKS'] = False
            can_castle['WQS'] = False

        if moving_piece == ChessPiece['BK']:
            can_castle['BKS'] = False
            can_castle['BQS'] = False

        new_turn = player_to_move.other_player()

        return ChessBoard(position=new_pos, player_to_move=new_turn, can_castle=can_castle, previous_move=move)

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

    def _squid(self, move):
        from_sq, to_sq = move
        piece = self.position[from_sq].name

        is_capture = self.position[to_sq] != ChessPiece['E']
        capture_string = 'x' if is_capture else ''
        desc = '' if piece in ['WP', 'BP'] and not is_capture else piece[1]
        return (f"{desc}{capture_string}{chr(96+to_sq[1]+1)}{to_sq[0]+1}")
