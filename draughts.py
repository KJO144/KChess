from base import Board, Player
from enum import Enum
from collections import defaultdict


class DraughtsPiece(Enum):

    B = ('B', 'BK', 0)
    W = ('W', 'WK', 7)
    BK = ('B', None, None)
    WK = ('W', None, None)
    E = (None, None, None)

    def __init__(self, owner_name, promotes_to_name, promotion_rank):
        self.owner_name = owner_name
        self.promotes_to_name = promotes_to_name
        self.promotion_rank = promotion_rank

    def promotes_to(self):
        """What does this piece promote to when it hits the back rank"""
        return DraughtsPiece[self.promotes_to_name]

    def __str__(self):
        return self.name

    def owner(self):
        if self.owner_name:
            return Player[self.owner_name]
        else:
            return None


def _initial_position():
    pos = {}
    for i in range(8):
        for j in range(8):
            square = (i, j)

            if (i+j) % 2 == 1 and i <= 2:
                p = DraughtsPiece['W']
            elif (i+j) % 2 == 1 and i >= 5:
                p = DraughtsPiece['B']
            else:
                p = DraughtsPiece['E']
            pos[square] = p
    return pos


def _captures_available(position, player_to_move, from_sq):
    "Are there captures available by the piece at from_sq"
    board = DraughtsBoard(position, player_to_move)
    legal_moves = board.legal_moves()

    captures = [move for move in legal_moves if move[0] == from_sq and abs(move[0][0]-move[1][0]) == 2]
    return len(captures) > 0


class DraughtsBoard(Board):

    instreams = ['player_to_move', 'position']
    _moves = {
            DraughtsPiece['W']: [(1, 1), (1, -1)],
            DraughtsPiece['B']: [(-1, -1), (-1, 1)],
            DraughtsPiece['WK']: [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            DraughtsPiece['BK']: [(1, 1), (1, -1), (-1, 1), (-1, -1)],
    }

    def __init__(self, position=_initial_position(), player_to_move=Player['W']):
        self.player_to_move = player_to_move
        self.position = position

    def legal_moves(self):
        """
        List of legal moves.
        A move is a pair of squares (from,to).
        """
        pos = self.position
        player_to_move = self.player_to_move
        other_player = player_to_move.other_player()
        regular_moves = []
        captures = []
        empty = DraughtsPiece['E']
        for from_sq, Piece in pos.items():
            if Piece.owner() == player_to_move:
                for (xm, ym) in self._moves[Piece]:
                    to_square = (from_sq[0] + xm, from_sq[1] + ym)
                    to_square_beyond = (to_square[0] + xm, to_square[1] + ym)
                    # regular moves
                    if pos.get(to_square) == empty:
                        regular_moves.append((from_sq, to_square))
                    # captures
                    if pos.get(to_square) is not None:
                        if pos.get(to_square).owner() == other_player and (pos.get(to_square_beyond) == empty):
                            captures.append((from_sq, to_square_beyond))
        if len(captures):
            lm = captures
        else:
            lm = regular_moves
        return lm

    def num_pieces(self):
        """Returns a dict mapping each piece to the counts of that piece on the board"""
        pos = self.position
        counts = defaultdict(int)
        for piece in pos.values():
            counts[piece] += 1
        return counts

    def winner(self):
        """
        There is a winner if one side has no pieces.
        """
        counts = self.num_pieces()
        nwhite = counts[DraughtsPiece['W']] + counts[DraughtsPiece['WK']]
        nblack = counts[DraughtsPiece['B']] + counts[DraughtsPiece['BK']]

        if nwhite == 0 and nblack != 0:
            return Player['B']
        elif nblack == 0 and nwhite != 0:
            return Player['W']
        else:
            return None

    def evaluation(self):
        """
        Returns a float representing the evaluation of the board position.
        Positive/negative if white/black has an advantage.
        """
        counts = self.num_pieces()
        W = counts[DraughtsPiece['W']] + 2*counts[DraughtsPiece['WK']]
        B = counts[DraughtsPiece['B']] + 2*counts[DraughtsPiece['BK']]

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

        is_promotion = (to_square[0] == moving_piece.promotion_rank)

        landing_piece = moving_piece if not is_promotion else moving_piece.promotes_to()

        new_pos[to_square] = landing_piece
        new_pos[from_square] = DraughtsPiece['E']

        is_capture = abs(to_square[1] - from_square[1]) == 2 and abs(to_square[0] - from_square[0]) == 2
        if is_capture:
            empty_square = ((to_square[0] + from_square[0])/2, (to_square[1] + from_square[1])/2)
            assert(new_pos[empty_square].owner() == player_to_move.other_player())
            new_pos[empty_square] = DraughtsPiece['E']

        new_player_to_move = player_to_move.other_player()

        # if there are more captures available with the same piece, then don't flip player_to_move
        is_multi_capture = is_capture and _captures_available(new_pos, player_to_move, to_square)
        new_player_to_move = player_to_move if is_multi_capture else player_to_move.other_player()

        return DraughtsBoard(new_pos, new_player_to_move)

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
