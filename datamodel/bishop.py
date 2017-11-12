from .piece import Piece
from .pawn import Pawn
from .game import Action, MoveResult


class Bishop(Pawn):
    def get_actions(self):
        actions = []
        
        for vector in ((1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0)):
            res = MoveResult(MoveResult.Type.REGULAR, self.pos)
            while True:
                res = self.game.step_move_to(self, res.pos, vector)
                if res.type == MoveResult.Type.INVALID:
                    break
                elif res.type == MoveResult.Type.REGULAR:
                    actions.append(Action("move", *res.pos))
                elif res.type == MoveResult.Type.CAPTURE:
                    actions.append(Action("move_capture", *res.pos))
                    break

        return actions