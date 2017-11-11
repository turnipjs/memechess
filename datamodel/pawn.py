from .piece import Piece
from .game import Action, Color


class Pawn(Piece):
	def get_actions(self):
		if self.color == Color.WHITE:
			direction = 1
		else:
			direction = -1
		actions = []#Action("move", self.x, self.y+1, self.z)]

		if self.game.is_valid_empty_space((self.x - direction, self.y, self.z)): #moves left or right
			actions.append(Action("move", self.x - direction, self.y, self.z))
		if self.game.is_valid_empty_space((self.x, self.y + direction, self.z)): #moves up or down
			actions.append(Action("move", self.x, self.y + direction, self.z))
		if self.game.is_valid_full_enemy_space((self.x -direction, self.y +direction, self.z), self.color): #captures diagonally
			actions.append(Action("move_capture", self.x - direction, self.y +direction, self.z))

		return actions


	def apply_action(self, action):
		if action.name == "move_capture":
			self.game.get_piece_at((action.x, action.y, action.z)).die()
		if action.name=="move" or action.name == "move_capture":
			self.x=action.x
			self.y=action.y
			self.z=action.z