from TTT import best_move, Board, Piece
import cProfile
import numpy as np

def game():
    pos = {i: Piece['E'] for i in range(9)}
#    pos[4] = Piece['W']
#    pos[3] = Piece['W']
    board = Board(pos, 'W')

    while not board.game_over():
        print(board)

        move = best_move(board)        
        board = board.make_move(move)    
        
        print("move: ", move[0], move[1])
        print("\n")

game()
