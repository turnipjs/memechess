import pygame
from datamodel import game, pawn, rook, bishop, queen, portal, king, pope, bowman, beekeeper, knight, highrise


SQUARE_SIZE=50

pygame.init()
screen = pygame.display.set_mode((20*SQUARE_SIZE, 20*SQUARE_SIZE))
ds
king_spots = (19, 0, 0)
queen_spot = (17, 1, 0)

def turnwise_symmetry(original):
	original = (19-original(1), 19-original(0), 0)
	return original

board = game.Game()

pieces_and_locations = []

'''
for each_piece in pieces_and_locations:
	board.add_piece(board)
	piece = piece 
'''

a=highrise.Highrise(board, (5, 5, 0), game.Color.WHITE)
board.add_piece(a)
b=highrise.Highrise(board, (6, 3, 0), game.Color.WHITE)
board.add_piece(b)



[board.add_piece(i) for i in portal.make_cave_pair(board, (13, 13, 0), (2, 2, 0))]
[board.add_piece(i) for i in portal.make_cave_pair(board, (13, 13, 1), (2, 2, 1))]

selected_piece = a

font = pygame.font.SysFont("monospace", 14)

run = True
while run:
	for e in pygame.event.get():
		if e.type==pygame.KEYDOWN:
			if e.key==pygame.K_q:
				run=False
		if e.type==pygame.MOUSEBUTTONDOWN:
			mx, my = pygame.mouse.get_pos()
			mx/=SQUARE_SIZE
			my/=SQUARE_SIZE
			mx = int(mx)
			my = int(my)
			if e.button==1:
				for z in range(100):
					print((mx, my, z))
					if board.has_piece((mx, my, z)):
						print("sel")
						selected_piece = board.get_piece_at((mx, my, z))
						break
			elif e.button==2:
				board.add_piece(eval(input("$"))(board, (mx, my, 0), game.Color.WHITE))
			elif e.button==3:
				board.start_turn(game.Color.WHITE)
				for action in actions:
					print(action, mx, my)
					if action.x==mx and action.y==my:
						print("apply")
						selected_piece.apply_action(action)
						break
			
	screen.fill((0,0,0))

	for x in range(0, 20):
		for y in range(0, 20):
			pygame.draw.rect(screen, (0,255,0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

	for piece in board.pieces:
		pygame.draw.rect(screen, [255,0,0] if piece.color == game.Color.BLACK else ([0,0,255] if piece.color == game.Color.WHITE else (100,100,100)),
			((piece.x*SQUARE_SIZE)+1, (piece.y*SQUARE_SIZE)+1, SQUARE_SIZE-2, SQUARE_SIZE-2), 0)
		screen.blit(font.render(type(piece).__name__, False, (255,255,255)),
			(piece.x*SQUARE_SIZE, piece.y*SQUARE_SIZE))
		screen.blit(font.render(piece.get_2nd_text(), False, (255, 255, 255)),
					(piece.x * SQUARE_SIZE, (piece.y * SQUARE_SIZE)+40))

	actions = selected_piece.get_actions()
	print("\n"*100)
	for i, action in enumerate(actions):
		screen.blit(font.render(action.name, False, (200,200,200)),
			(action.x*SQUARE_SIZE, (action.y*SQUARE_SIZE)+10+(10 if "_" in action.name else 0)))
	print("\n".join(str(s) for s in board.pieces))

	pygame.display.flip()