from .piece import Piece
from .game import Action, MoveResult, Color

class PortalExit(Piece):
	can_capture = False

	def _get_actions(self):
		actions = []

		for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0),
					   (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
			res = self.game.step_move_to(self, self.pos, vector)
			if res.type == MoveResult.Type.REGULAR:
				actions.append(Action("move", *res.pos))

		return actions

	def apply_action(self, action):
		if action.name=="move":
			self.pos = action[1:]

class PortalEntrance(PortalExit):
	can_land_on = True
	preserves_speed = False

	def __init__(self, game, pos, color, exit):
		Piece.__init__(self, game, pos, color)
		self.exit = exit

	def step_move_into(self, piece, pos, direction):
		end_point = [self.exit.pos[0]+direction[0], self.exit.pos[1]+direction[1], self.exit.pos[2]+direction[2]]
		if self.game.has_piece(end_point) and self.game.get_piece_at(end_point).can_be_captured:
			return MoveResult(MoveResult.Type.CAPTURE, end_point)
		elif self.game.valid_location(end_point):
			return MoveResult(MoveResult.Type.REGULAR, end_point, ends_motion = not self.preserves_speed)

class CavePortal(PortalEntrance):
	preserves_speed = True
	can_be_captured = False

def make_cave_pair(game, pos1, pos2):
	a = CavePortal(game, pos1, Color.NONE, None)
	b = CavePortal(game, pos2, Color.NONE, a)
	a.exit = b
	return (a, b)