from .piece import Piece
from .game import Action, MoveResult
from .king import King
from .queen import Queen
import random

class Beekeeper(Piece):
	identifier = "beekeeper"
	
	def _get_actions(self):
		actions = [Action("release_swarm", *self.pos)]
		for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0),
				   (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
			res = self.game.step_move_to(self, self.pos, vector)
			if res.type == MoveResult.Type.REGULAR:
				actions.append(Action("move", *res.pos))
				if res.ends_motion:
					continue
			elif res.type == MoveResult.Type.CAPTURE:
				actions.append(Action("capture", *res.pos))
			else:
				continue

			step2 = self.game.step_move_to(self, res.pos, vector)

			if step2.type == MoveResult.Type.REGULAR:
				actions.append(Action("move", *step2.pos))

		return actions

	def apply_action(self, action):
		if action.name=="move":
			self.pos=action[1:]
		elif action.name=="capture":
			self.game.get_piece_at(action[1:]).die()
		elif action.name=="release_swarm":
			x = random.randint(0, 19)
			y = random.randint(0, 19)
			for z in range(5):
				if self.game.has_piece((x, y, z)):
					p = self.game.get_piece_at((x, y, z))
					if type(p) is King or type(p) is Queen:
						pass
					else:
						p.die()
