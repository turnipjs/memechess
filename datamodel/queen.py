from .piece import Piece
from .rook import Rook
from .bishop import Bishop

class Queen(Rook):
	identifier = "queen"
	
	def _get_actions(self):
		return Rook._get_actions(self) + Bishop._get_actions(self)