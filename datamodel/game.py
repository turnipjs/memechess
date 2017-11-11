import enum
import collections

Action = collections.namedtuple("Action", ["name", "x", "y", "z"])

class Color(enum.Enum):
	NONE=0
	BLACK=1
	WHITE=2

class Game:
	def __init__(self):
		self.pieces = []

	def get_piece_at(self, pos):
		pos = tuple(pos)
		for piece in self.pieces:
			if piece.pos == pos:
				return piece
		raise IndexError("No piece at "+str(pos))

	def has_piece(self, pos):
		for piece in self.pieces:
			if piece.pos == pos:
				return True
		return False

	def valid_location(self, pos):
		if 0 <= pos[0] <= 19:
			if 0 <= pos[1] <= 19:
				return True
		return False

	def is_valid_empty_space(self, pos):
		if self.valid_location(pos):
			return not self.has_piece(pos)
		return False

	def is_valid_full_space(self, pos):
		if self.valid_location(pos):
			return self.has_piece(pos)
		return False

	def is_valid_full_enemy_space(self, pos, my_color):
		if self.valid_location(pos):
			if self.has_piece(pos):
				return self.get_piece_at(pos).color != my_color
		return False

	def add_piece(self, piece):
		self.pieces.append(piece)
