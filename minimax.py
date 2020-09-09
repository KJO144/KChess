from base import Board, Player
import numpy as np

def minimax(board, move, max_depth=None):
    """Returns a score for move."""
    
    player_to_move = board.player_to_move
    new_board = board.make_move(move)
    
    winner = new_board.winner()
    
    if winner is not None:
        assert(player_to_move == winner)
        return winner.top_score

    if max_depth == 0:
        return new_board.evaluation()

    legal_moves = new_board.legal_moves()
    
    if len(legal_moves) == 0:
        return(0)

    if max_depth:
        max_depth -= 1

    scores = [minimax(new_board, lm, max_depth) for lm in legal_moves]
    
    if player_to_move == Player['W']:
        ret = min(scores)
    if player_to_move == Player['B']:
        ret = max(scores)

    return(ret)

def best_move(board, max_depth=None):
    """
    Returns the best move on the board.
    """

    legal_moves = board.legal_moves()
    
    scores = np.array([minimax(board, move, max_depth) for move in legal_moves])
    if board.player_to_move == Player['W']:
        index = scores.argmax()
    else:
        index = scores.argmin()

    return legal_moves[index]
