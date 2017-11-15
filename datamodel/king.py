from .pawn import Pawn
from .game import Action, MoveResult

class King(Pawn):
	identifier = "king"
	
	def _get_actions(self):
		actions = []
		for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0),
				   (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
			res = self.game.step_move_to(self, self.pos, vector)
			if res.type == MoveResult.Type.REGULAR:
				actions.append(Action("move", *res.pos))
			elif res.type == MoveResult.Type.CAPTURE:
				actions.append(Action("move_capture", *res.pos))

		return actions
