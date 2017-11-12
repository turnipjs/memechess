from .king import King
from .queen import Queen
from .game import Action, MoveResult

class Pope(King):
	def __init__(self, game, pos, color):
		King.__init__(self, game, pos, color)
		self.is_jetpack = False
		self.attacking = None
		self.attacking_turns_remaining = 3

	def get_actions(self):
		if can_move == True:
			if self.attacking:
				return []
			if not self.is_jetpack:
				return King.get_actions(self) + [Action("pray_for_jetpack", *self.pos)]
			else:
				actions = [action for action in Queen.get_actions(self) if action.name!="move_capture"]
				enemies = []
				to_remove = set()
				for action in actions:
					for z in range(5):
						if self.game.is_valid_full_enemy_space((action.x, action.y, z), self.color):
							enemies.append((action.x, action.y, z))
							to_remove = to_remove | {action}
				for a in to_remove:
					actions.remove(a)
				for e in enemies:
					actions.append(Action("pope_attack", *e))

				ok = True
				for z in range(5):
					if not self.game.is_valid_empty_space((self.x, self.y, z)):
						ok = False

				if ok:
					actions.append(Action("damn_jetpack", *self.pos))
			return actions

	def apply_action(self, action):
		if action.name == "pray_for_jetpack":
			self.is_jetpack = True
			self.z = 5
		if action.name == "damn_jetpack":
			self.is_jetpack = False
			self.z = 0
		if action.name == "pope_attack":
			self.attacking = self.game.get_piece_at(action[1:])
			self.attacking_turns_remaining = 3
			self.attacking.z = -1
			self.pos = self.attacking.pos
			self.z = 0
		if action.name == "move_capture":
			self.game.get_piece_at((action.x, action.y, action.z)).die()
		if action.name=="move" or action.name == "move_capture":
			self.pos = action[1:]

	def on_owner_turn_start(self):
		if self.attacking:
			self.attacking_turns_remaining-=1
			if self.attacking_turns_remaining==0:
				self.attacking.die()
				self.attacking=None
				self.z = 5

	def __str__(self):
		return f"<Pope {self.pos} {self.is_jetpack} {self.color} {self.attacking}:{self.attacking_turns_remaining}>"
