from flask import Flask
from flask_cors import CORS, cross_origin
from draughts import DraughtsBoard, DraughtsPiece
from chess import ChessBoard, ChessPiece
from minimax import best_move
from base import Player
import json

board_types = {'draughts': DraughtsBoard, 'chess': ChessBoard}
piece_types = {'draughts': DraughtsPiece, 'chess': ChessPiece}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def json_to_board(game, board_position_json):

    board_position = json.loads(board_position_json)

    board_position['player_to_move'] = Player[board_position['player_to_move']]

    board_type = board_types[game]
    piece_type = piece_types[game]

    bp = board_position['position']
    board_position['position'] = {(int(sq[1]), int(sq[2])): piece_type[piece] for sq, piece in bp.items()}

    pm = board_position['previous_move']
    if pm != "none":
        board_position['previous_move'] = ((int(pm[1]), int(pm[2])), (int(pm[4]), int(pm[5])))

    if board_position.get('move'):
        del(board_position['move'])

    board = board_type.from_dict(board_position)
    return board


@app.route('/<game>/initial_position')
@cross_origin()
def initial_position(game):
    board_type = board_types[game]
    b = board_type()
    return b.to_json()


@app.route('/<game>/pos/<position_json>')
@cross_origin()
def make_move_given_position(game, position_json):
    "Given a position, find the best move and return the new board with that move played."

    board = json_to_board(game, position_json)

    move = best_move(board, 2)
    new_board = board.make_move(move)

    ret = new_board.to_json()

    return ret


@app.route('/<game>/move/<pos_and_move_json>')
@cross_origin()
def play_move(game, pos_and_move_json):
    """
    Given a position and a move, play that move and return the new board.
    If the move is illegal, just return the original position.
    The move is in the format S13_S34
    """
    board = json_to_board(game, pos_and_move_json)

    move = json.loads(pos_and_move_json)['move']

    move = ((int(move[1]), int(move[2])), (int(move[5]), int(move[6])))

    legal_moves = board.legal_moves()

    if move in legal_moves:
        new_board = board.make_move(move)
    else:
        print(move, ' is not legal.')
        new_board = board

    ret = new_board.to_json()
    return ret


if __name__ == "__main__":
    app.run()
