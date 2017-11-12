from .piece import Piece
from .game import Action, Color, MoveResult


class Pawn(Piece):
	def get_actions(self):
		if self.color == Color.WHITE:
			direction = 1
		else:
			direction = -1
		actions = []

		if can_move == True:
			res = self.game.step_move_to(self, self.pos, (-direction, 0, 0))
			if res.type == MoveResult.Type.REGULAR:
				actions.append(Action("move", *res.pos))

			res = self.game.step_move_to(self, self.pos, (0, direction, 0))
			if res.type == MoveResult.Type.REGULAR:
				actions.append(Action("move", *res.pos))

			res = self.game.step_move_to(self, self.pos, (-direction, direction, 0))
			if res.type == MoveResult.Type.CAPTURE:
				actions.append(Action("move_capture", *res.pos))

		return actions

	def apply_action(self, action):
		if action.name == "move_capture":
			self.game.get_piece_at((action.x, action.y, action.z)).die()
		if action.name=="move" or action.name == "move_capture":
			self.pos = action[1:]
