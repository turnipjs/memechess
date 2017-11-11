from .piece import Piece
from .game import Action

class Pawn(Piece):
	def get_actions(self):
		return [Action("move", self.x, self.y+1, self.z)]

	def apply_action(self, action):
		if action.name=="move":
			self.x=action.x
			self.y=action.y
			self.z=action.z