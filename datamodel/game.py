import enum
import collections

Action = collections.namedtuple("Action", ["name", "x", "y", "z"])

class Color(enum.Enum):
	NONE=0
	BLACK=1
	WHITE=2

class MoveResultType(enum.Enum):
	INVALID=0
	CAPTURE=1
	REGULAR=2

MoveResult = collections.namedtuple("MoveResult", ["type", "pos"])
MoveResult.Type = MoveResultType

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

	def step_move_to(self, peice, pos, direction):
		new_location = (pos[0]+direction[0], pos[1]+direction[1], pos[2]+direction[2])
		if self.is_valid_empty_space(new_location):
			return MoveResult(MoveResult.Type.REGULAR, new_location)
		if self.has_piece(new_location):
			target = self.get_piece_at(new_location)
			if target.color == Color.NONE or target.color == peice.color:
				if target.can_land_on:
					return MoveResult(MoveResult.Type.REGULAR, target.step_move_into(peice, pos, direction))
				else:
					return MoveResult(MoveResult.Type.INVALID, 0)
			elif peice.can_capture: #enemy peice
				return MoveResult(MoveResult.Type.CAPTURE, new_location)
		return MoveResult(MoveResult.Type.INVALID, 0)
