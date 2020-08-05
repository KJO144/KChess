from TTT import minimax, Board, Piece

pB = Piece('B')
pW = Piece('W')
pE = Piece('E')

pos = {i: pE for i in range(9)}

#pos[0] = pW
# pos[1] = pB
# pos[2] = pW
# pos[4] = pB
#pos[3] = pW
#pos[8] = pB
#pos[0] = pB

board = Board(pos, 'W')

print(board)
legal_moves = board.legal_moves()

score = [minimax(board, move) for move in legal_moves]

for (sq,p),s in zip(legal_moves, score):
    print(sq, p, s)