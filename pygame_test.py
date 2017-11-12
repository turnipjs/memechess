import pygame
from datamodel import game, pawn, rook, bishop, queen

SQUARE_SIZE=50

pygame.init()
screen = pygame.display.set_mode((20*SQUARE_SIZE, 20*SQUARE_SIZE))

board = game.Game()
a=queen.Queen(board, (5, 5, 0), game.Color.BLACK)
board.add_piece(a)
b=pawn.Pawn(board, (6, 4, 0), game.Color.WHITE)
board.add_piece(b)

SELECTED_PIECE = a

font = pygame.font.SysFont("monospace", 12)

run = True
while run:
	for e in pygame.event.get():
		if e.type==pygame.KEYDOWN:
			if e.key==pygame.K_q:
				run=False
			
	screen.fill((0,0,0))

	for x in range(0, 20):
		for y in range(0, 20):
			pygame.draw.rect(screen, (0,255,0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

	for piece in board.pieces:
		pygame.draw.rect(screen, [255,0,0] if piece.color == game.Color.BLACK else [0,0,255],
			((piece.x*SQUARE_SIZE)+1, (piece.y*SQUARE_SIZE)+1, SQUARE_SIZE-2, SQUARE_SIZE-2), 0)
		screen.blit(font.render(type(piece).__name__, False, (255,255,255)),
			(piece.x*SQUARE_SIZE, piece.y*SQUARE_SIZE))

	print("\n"*100)
	actions=SELECTED_PIECE.get_actions()
	for i, action in enumerate(actions):
		print(i, ": ", action)
		screen.blit(font.render(action.name+"["+str(i)+"]", False, (200,200,200)),
			(action.x*SQUARE_SIZE, (action.y*SQUARE_SIZE)+10))

	pygame.display.flip()
	SELECTED_PIECE.apply_action(actions[int(input(">"))])