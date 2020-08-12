from TTT import TTTBoard
from draghts import DraughtsBoard
from minimax import best_move
import cProfile
import numpy as np

initial_board = TTTBoard()
def game(board):
    
    while not board.game_over():

        move = best_move(board)        
        board = board.make_move(move)    
        
        print(board)
        #print("move: ", move[0], move[1])
        print("\n")

game(initial_board)
#initial_board = DraughtsBoard()
