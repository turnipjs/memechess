
class Piece:
	def __init__(self, game, pos, color):
		self.game = game
		self.pos = pos
		self.color = color

	@property
	def x(self): return self.pos[0]
	@x.setter
	def x(self, x): self.pos[0]=x

	@property
	def y(self): return self.pos[1]
	@y.setter
	def y(self, x): self.pos[1]=x

	@property
	def z(self): return self.pos[2]
	@z.setter
	def z(self, x): self.pos[2]=x

	def __str__(self):
		return "<"+type(self).__name__+" "+str(self.pos)+" "+str(self.color)+">"

	def get_actions(self):
		return []

	def apply_action(self):
		raise NotImplemented()