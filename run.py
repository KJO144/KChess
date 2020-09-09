from TTT import TTTBoard
from draughts import DraughtsBoard, DraughtsPiece
from chess import ChessBoard, ChessPiece
from minimax import best_move, minimax
from base import Player
import cProfile
import numpy as np



def game(board, max_depth=None, num_moves=100):
    moves = 0
    while moves<num_moves:

        move = best_move(board, max_depth)        
        board = board.make_move(move)
        moves += 1
        
        print(board)
        #print("move: ", move[0], move[1])
        print("\n")

#b = TTTBoard()
b = DraughtsBoard()
game(b,2, 4)
#print(b.legal_moves())
#rint(b)
#cProfile.run("game(b,2, 4)")
#print(b.evaluation())
