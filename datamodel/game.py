import enum
import collections

class Action(collections.namedtuple("Action", ["name", "x", "y", "z"])):
	def to_json(self):
		return {
			"name": self.name,
			"pos": self[1:]
		}

class ILLEGALPOS_OOB:pass
class ILLEGALPOS_FULL:pass

class Color(enum.Enum):
	NONE=0
	BLACK=1
	WHITE=2

	def opposite(self):
		if self==self.WHITE:
			return self.BLACK
		return self.WHITE

	def to_json_string(self):
		if self==self.WHITE: return "WHITE"
		if self==self.BLACK: return "BLACK"
		return "NONE"

#MoveResult = collections.namedtuple("MoveResult", ["type", "pos"])
class MoveResult:
	class Type(enum.Enum):
		INVALID=0
		CAPTURE=1
		REGULAR=2
		
	def __init__(self, type, pos, ends_motion=False):
		self.type = type
		self.pos = pos
		self.ends_motion = ends_motion

	def __str__(self):
		return "MoveResult("+",".join(str(i) for i in (self.type, self.pos, self.ends_motion))+")"
	def __repr__(self): return str(self)

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
				return self.get_piece_at(pos).color == my_color.opposite()
		return False

	def add_piece(self, piece):
		self.pieces.append(piece)

	def step_move_to(self, peice, pos, direction):
		new_location = (pos[0]+direction[0], pos[1]+direction[1], pos[2]+direction[2])
		if self.is_valid_empty_space(new_location):
			return MoveResult(MoveResult.Type.REGULAR, new_location)
		if self.has_piece(new_location):
			target = self.get_piece_at(new_location)
			if peice.can_capture and target.color != peice.color and target.can_be_captured: #enemy peice
				return MoveResult(MoveResult.Type.CAPTURE, new_location)
			elif target.color == Color.NONE or target.color == peice.color:
				if target.can_land_on:
					return target.step_move_into(peice, pos, direction)
				else:
					return MoveResult(MoveResult.Type.INVALID, ILLEGALPOS_FULL())
		return MoveResult(MoveResult.Type.INVALID, ILLEGALPOS_OOB())

	def start_turn(self, color):
		for piece in self.pieces:
			if piece.color == color:
				piece.on_owner_turn_start()

	def to_json(self):
		return {
			"pieces": [p.to_json() for p in self.pieces]
		}