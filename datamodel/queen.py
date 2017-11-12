from .piece import Piece
from .rook import Rook
from .bishop import Bishop

class Queen(Rook):
	def get_actions(self):
		return Rook.get_actions(self) + Bishop.get_actions(self)