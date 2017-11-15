from datamodel import game, pawn, rook, bishop, queen, portal, king, pope, bowman, beekeeper, knight, highrise

def turnwise_symmetry(original):
	base = (19-original[0], 19-original[1], 0)
	return base

def create():
	board = game.Game()
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

	pieces_and_locations = []

	pieces_and_locations.append(king.King(board, king_coords, game.Color.WHITE))
	pieces_and_locations.append(king.King(board, turnwise_symmetry(king_coords), game.Color.BLACK))

	pieces_and_locations.append(queen.Queen(board, queen_coords, game.Color.WHITE))
	pieces_and_locations.append(queen.Queen(board, turnwise_symmetry(queen_coords), game.Color.BLACK))

	pieces_and_locations.append(pope.Pope(board, pope_coords, game.Color.WHITE))
	pieces_and_locations.append(pope.Pope(board, turnwise_symmetry(pope_coords), game.Color.BLACK))

	for i in pawn_coords:
		pieces_and_locations.append(pawn.Pawn(board, i, game.Color.WHITE))
		pieces_and_locations.append(pawn.Pawn(board, turnwise_symmetry(i), game.Color.BLACK))

	for i in bishop_coords:
		pieces_and_locations.append(bishop.Bishop(board, i, game.Color.WHITE))
		pieces_and_locations.append(bishop.Bishop(board, turnwise_symmetry(i), game.Color.BLACK))

	for i in knight_coords:
		pieces_and_locations.append(knight.Knight(board, i, game.Color.WHITE))
		pieces_and_locations.append(knight.Knight(board, turnwise_symmetry(i), game.Color.BLACK))

	for i in rook_coords:
		pieces_and_locations.append(rook.Rook(board, turnwise_symmetry(i), game.Color.WHITE))
		pieces_and_locations.append(rook.Rook(board, i, game.Color.BLACK))

	for each_piece in pieces_and_locations:
		board.add_piece(each_piece)

	for i in range(0, 7):
		[board.add_piece(i) for i in portal.make_cave_pair(board, (9, 6, i), (9, 13, i))]
		[board.add_piece(i) for i in portal.make_cave_pair(board, (10, 6, i), (10, 13, i))]
		[board.add_piece(i) for i in portal.make_cave_pair(board, (6, 10, i), (13, 10, i))]
		[board.add_piece(i) for i in portal.make_cave_pair(board, (6, 9, i), (13, 9, i))]

	return board

def create():
	board = game.Game()
	board.add_piece(pope.Pope(board, (1,1,0), game.Color.WHITE))
	board.add_piece(pawn.Pawn(board, (3,3,0), game.Color.BLACK))
	return board