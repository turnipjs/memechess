import pygame
from datamodel import game, pawn, rook, bishop, queen, portal, king, pope, bowman, beekeeper, knight, highrise


SQUARE_SIZE=50

pygame.init()
screen = pygame.display.set_mode((20*SQUARE_SIZE, 20*SQUARE_SIZE))

def turnwise_symmetry(original):
	base = (19-original[0], 19-original[1], 0)
	return base

""" LEGIT ACTUAL COORDS NOT THE BOOTLEGGED ONES WE DID FOR THE EXPO
king_coords = (0, 19, 0)
queen_coords = (1, 17, 0)
pope_coords = (2, 19, 0)


pawn_coords = [(2, 15, 0), (2, 14, 0), (2, 13, 0), (2, 12, 0), (2, 11, 0),
			   (4, 17, 0), (5, 17, 0), (6, 17, 0), (7, 17, 0), (8, 17, 0)]
bishop_coords = [(0, 15, 0), (1, 15, 0), (4, 19, 0), (4, 18, 0)]
knight_coords = [(10, 18, 0), (1, 10, 0)]
rook_coords = [(16, 0, 0), (19, 3, 0)]
beekeeper_coords = []
bowman_coords = []
mage_coords = []

"""

king_coords = (0, 19, 0)
queen_coords = ()

board = game.Game()

pieces_and_locations = []

# #pieces_and_locations.append(king.King(board, king_coords, game.Color.WHITE))
# pieces_and_locations.append(king.King(board, turnwise_symmetry(king_coords), game.Color.BLACK))

# pieces_and_locations.append(queen.Queen(board, queen_coords, game.Color.WHITE))
# pieces_and_locations.append(queen.Queen(board, turnwise_symmetry(queen_coords), game.Color.BLACK))

# pieces_and_locations.append(pope.Pope(board, pope_coords, game.Color.WHITE))
# pieces_and_locations.append(pope.Pope(board, turnwise_symmetry(pope_coords), game.Color.BLACK))

# for i in pawn_coords:
# 	pieces_and_locations.append(pawn.Pawn(board, i, game.Color.WHITE))
# 	pieces_and_locations.append(pawn.Pawn(board, turnwise_symmetry(i), game.Color.BLACK))

# for i in bishop_coords:
# 	pieces_and_locations.append(bishop.Bishop(board, i, game.Color.WHITE))
# 	pieces_and_locations.append(bishop.Bishop(board, turnwise_symmetry(i), game.Color.BLACK))

# for i in knight_coords:
# 	pieces_and_locations.append(knight.Knight(board, i, game.Color.WHITE))
# 	pieces_and_locations.append(knight.Knight(board, turnwise_symmetry(i), game.Color.BLACK))

# for i in rook_coords:
# 	pieces_and_locations.append(rook.Rook(board, turnwise_symmetry(i), game.Color.WHITE))
# 	pieces_and_locations.append(rook.Rook(board, i, game.Color.BLACK))



#pieces_and_locations.append()

for each_piece in pieces_and_locations:
	board.add_piece(each_piece)

a=king.King(board, king_coords, game.Color.WHITE)
board.add_piece(a)



for i in range(0, 7):
	[board.add_piece(i) for i in portal.make_cave_pair(board, (9, 6, i), (9, 13, i))]
	[board.add_piece(i) for i in portal.make_cave_pair(board, (10, 6, i), (10, 13, i))]
	[board.add_piece(i) for i in portal.make_cave_pair(board, (6, 10, i), (13, 10, i))]
	[board.add_piece(i) for i in portal.make_cave_pair(board, (6, 9, i), (13, 9, i))]


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
		screen.blit(font.render(piece.get_desc_text(), False, (255, 255, 255)),
					(piece.x * SQUARE_SIZE, (piece.y * SQUARE_SIZE)+40))

	actions = selected_piece.get_actions()
	print("\n"*100)
	for i, action in enumerate(actions):
		screen.blit(font.render(action.name, False, (200,200,200)),
			(action.x*SQUARE_SIZE, (action.y*SQUARE_SIZE)+10+(10 if "_" in action.name else 0)))
	print("\n".join(str(s) for s in board.pieces))

	pygame.display.flip()