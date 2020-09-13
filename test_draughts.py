from draughts import DraughtsBoard, DraughtsPiece
from base import Player

W = DraughtsPiece['W']
B = DraughtsPiece['B']
E = DraughtsPiece['E']


def empty_position():
    position = {}
    for i in range(8):
        for j in range(8):
            position[(i, j)] = E
    return position


def test_simple_capture():
    """
    Simple position with single capture.
    There should be only one legal move. The player_to_move should
    flip from W to B.
    """
    position = empty_position()
    position[(2, 2)] = W
    position[(3, 3)] = B

    b = DraughtsBoard(position=position, player_to_move=Player['W'])
    capture = ((2, 2), (4, 4))
    assert [capture] == b.legal_moves()
    nb = b.make_move(capture)
    assert nb.player_to_move == Player['B']


def test_simple_multi_capture():
    """
    Simple position with multi capture. After the first capture the
    player_to_move should not flip, and the only legal move should be
    the second capture.
    """
    position = empty_position()
    position[(2, 2)] = W
    position[(3, 3)] = B
    position[(5, 5)] = B

    b = DraughtsBoard(position=position, player_to_move=Player['W'])

    first_capture = ((2, 2), (4, 4))
    assert [first_capture] == b.legal_moves()
    nb = b.make_move(first_capture)
    assert nb.player_to_move == Player['W']

    second_capture = ((4, 4), (6, 6))
    assert [second_capture] == nb.legal_moves()
    nb2 = nb.make_move(second_capture)
    assert nb2.player_to_move == Player['B']


def test_complex_multi_capture():
    """
    Position where there is both a multi capture and a separate single
    capture available.
    """
    position = empty_position()
    position[(2, 2)] = W  # c3
    position[(3, 3)] = B  # d4
    position[(5, 5)] = B  # f6

    position[(0, 4)] = W  # e1
    position[(1, 5)] = B  # f2

    b = DraughtsBoard(position=position, player_to_move=Player['W'])

    capture11 = ((2, 2), (4, 4))  # c3-e5
    capture12 = ((4, 4), (6, 6))  # e5-g7
    capture2 = ((0, 4), (2, 6))   # e1-g3
    lm = b.legal_moves()
    assert sorted([capture11, capture2]) == sorted(lm)
    nb = b.make_move(capture11)
    assert nb.player_to_move == Player['W']

    lm = nb.legal_moves()
    assert [capture12] == lm
