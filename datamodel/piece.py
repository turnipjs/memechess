
class Piece:
	can_land_on = False
	can_capture = True

	def __init__(self, game, pos, color):
		self.game = game
		self.pos = pos
		self.color = color

	@property
	def pos(self): return (self.x, self.y, self.z)
	@pos.setter
	def pos(self, new):
		self.x, self.y, self.z = new

	def __str__(self):
		return "<"+type(self).__name__+" "+str(self.pos)+" "+str(self.color)+">"

	def __repr__(self): return str(self)

	def get_actions(self):
		return []

	def apply_action(self):
		raise NotImplemented()

	def die(self):
		self.game.pieces.remove(self)

	def step_move_into(self, peice, pos, direction):
		raise NotImplemented()