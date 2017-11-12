import pygame
from datamodel import game, pawn, rook, bishop, queen, portal, king, pope, knight

SQUARE_SIZE=50

pygame.init()
screen = pygame.display.set_mode((20*SQUARE_SIZE, 20*SQUARE_SIZE))

board = game.Game()
a=knight.Knight(board, (5, 5, 0), game.Color.WHITE)
board.add_piece(a)
b=portal.PortalExit(board, (6, 3, 0), game.Color.WHITE)
board.add_piece(b)

board.add_piece(portal.PortalEntrance(board, (10, 10, 0), game.Color.WHITE, b))
board.add_piece(pawn.Pawn(board, (10, 7, 0), game.Color.BLACK))

[board.add_piece(i) for i in portal.make_cave_pair(board, (13, 13, 0), (2, 2, 0))]
[board.add_piece(i) for i in portal.make_cave_pair(board, (13, 13, 1), (2, 2, 1))]

selected_piece = a

font = pygame.font.SysFont("monospace", 12)

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
			# print(e, e.button)
			# input()
			if e.button==1:
				for z in range(100):
					print((mx, my, z))
					if board.has_piece((mx, my, z)):
						print("sel")
						selected_piece = board.get_piece_at((mx, my, z))
						break
			elif e.button==3:
				board.start_turn(game.Color.WHITE)
				for action in actions:
					print(action, mx, my)
					if action.x==mx and action.y==my:
						print("apply")
						selected_piece.apply_action(action)
						break
				# input()
			# print("done, p=", pressed, "mx, my = ", mx, my)
			# input()
			
	screen.fill((0,0,0))

	for x in range(0, 20):
		for y in range(0, 20):
			pygame.draw.rect(screen, (0,255,0), (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

	for piece in board.pieces:
		pygame.draw.rect(screen, [255,0,0] if piece.color == game.Color.BLACK else ([0,0,255] if piece.color == game.Color.WHITE else (100,100,100)),
			((piece.x*SQUARE_SIZE)+1, (piece.y*SQUARE_SIZE)+1, SQUARE_SIZE-2, SQUARE_SIZE-2), 0)
		screen.blit(font.render(type(piece).__name__, False, (255,255,255)),
			(piece.x*SQUARE_SIZE, piece.y*SQUARE_SIZE))

	actions = selected_piece.get_actions()
	print("\n"*100)
	for i, action in enumerate(actions):
		screen.blit(font.render(action.name+"["+str(i)+"]", False, (200,200,200)),
			(action.x*SQUARE_SIZE, (action.y*SQUARE_SIZE)+10))
	print("\n".join(str(s) for s in board.pieces))

	pygame.display.flip()