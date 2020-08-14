from TTT import TTTBoard
from draghts import DraughtsBoard, DraughtsPiece
from minimax import best_move, minimax
from base import Player
import cProfile
import numpy as np



def game(board, max_depth=None):
    
    while not board.game_over():

        move = best_move(board, max_depth)        
        board = board.make_move(move)    
        
        print(board)
        #print("move: ", move[0], move[1])
        print("\n")

b = TTTBoard()
#b = DraughtsBoard()

game(b)
#print(b.evaluation())
