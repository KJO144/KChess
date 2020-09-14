from chess import ChessBoard, ChessPiece
from base import Player


E = ChessPiece['E']


def empty_position():
    position = {}
    for i in range(8):
        for j in range(8):
            position[(i, j)] = E
    return position


def test_starting_pos_legal_moves():
    """Check that there are 20 legal moves in the starting position"""
    b = ChessBoard()
    lm = b.legal_moves()

    assert len(lm) == 20


def test_castling_KS():
    """Test king side castling."""
    b = ChessBoard()
    b = b.make_move(((1, 4), (3, 4)))  # e4
    b = b.make_move(((6, 4), (4, 4)))  # e5
    b = b.make_move(((0, 6), (2, 5)))  # Nf3
    b = b.make_move(((7, 6), (5, 5)))  # Nf6
    b = b.make_move(((0, 5), (3, 2)))  # Bc4
    b = b.make_move(((7, 5), (4, 2)))  # Bc5

    # check white can castle now
    white_castle = ((0, 4), (0, 6))
    legal_moves = b.legal_moves()
    assert white_castle in legal_moves

    b = b.make_move(((0, 4), (1, 4)))  # Ke2

    # check black can castle now
    black_castle = ((7, 4), (7, 6))
    assert(black_castle in b.legal_moves())

    b = b.make_move(((7, 4), (6, 4)))  # Ke7

    b = b.make_move(((1, 4), (0, 4)))  # Ke1
    b = b.make_move(((6, 4), (7, 4)))  # Ke8

    # check white cannot castle
    assert white_castle not in b.legal_moves()

    b = b.make_move(((0, 1), (2, 2)))  # Nc3

    # check black cannot castle
    assert black_castle not in b.legal_moves()


def test_promotion():
    """
    When pawns reach the back rank they should become queens (currently we don't support under-promotion).
    When other pieces move to the back rank, they should remain as themselves.
    """
    position = empty_position()
    position[(6, 0)] = ChessPiece['WP']  # a7
    position[(1, 4)] = ChessPiece['BP']  # e2
    position[(0, 0)] = ChessPiece['WK']  # a1
    position[(0, 7)] = ChessPiece['BK']  # h1
    position[(5, 5)] = ChessPiece['WB']  # f6
    position[(1, 6)] = ChessPiece['BR']  # g2
    can_castle = {'WKS': False, 'WQS': False, 'BKS': False, 'BQS': False}
    board = ChessBoard(position=position, can_castle=can_castle, last_move=None, player_to_move=Player['W'])

    nb = board.make_move(((6, 0), (7, 0)))  # a8=Q
    assert nb.position[(7, 0)] == ChessPiece['WQ'], "white promotion"

    nb = board.make_move(((5, 5), (7, 3)))  # Bd8
    assert nb.position[(7, 3)] == ChessPiece['WB'], "white piece moves to back rank"

    nb2 = nb.make_move(((1, 4), (0, 4)))  # e1=Q
    assert nb2.position[(0, 4)] == ChessPiece['BQ'], "black promotion"

    nb2 = nb.make_move(((1, 6), (0, 6)))  # Rg1
    assert nb2.position[(0, 6)] == ChessPiece['BR'], "black piece moves to back rank"
