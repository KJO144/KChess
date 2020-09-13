from chess import ChessBoard


def test_starting_pos_legal_moves():
    """Check that there are 20 legal moves in the starting position"""
    b = ChessBoard()
    lm = b.legal_moves()

    assert len(lm) == 20


def test_castling_WKS():
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
