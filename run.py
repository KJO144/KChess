from TTT import minimax, Board, Piece
import cProfile

def run():

    pE = Piece['E']

    pos = {i: pE for i in range(9)}
    #pos[4] = pW
    board = Board(pos, 'B')

    legal_moves = board.legal_moves()

    score = [minimax(board, move) for move in legal_moves]
    for (sq,p),s in zip(legal_moves, score):
        print(sq, p, s)


cProfile.run("run()")
#run()