from TTT import best_move, Board, Piece, Player
import cProfile
import numpy as np

def game():
    pos = {i: Piece['E'] for i in range(9)}
    board = Board(pos, Player['W'])

    while not board.game_over():

        move = best_move(board)        
        board = board.make_move(move)    
        
        print(board)
        print("move: ", move[0], move[1])
        print("\n")

game()
