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
		for piece in self.pieces:
			if piece.pos == pos:
				return piece
		raise IndexError("No piece at "+str(pos))

	def has_piece(self, pos):
		for piece in self.pieces:
			if piece.pos == pos:
				return True
		return False

	def add_piece(self, piece):
		self.pieces.append(piece)

