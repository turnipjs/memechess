from .piece import Piece
from .game import Action, MoveResult

class Bowman(Piece):
    identifier = "bowman"
    
    def _get_actions(self):
        actions = []
        for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0),
                    (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
            res = self.game.step_move_to(self, self.pos, vector)
            if res.type == MoveResult.Type.REGULAR:
                actions.append(Action("move", *res.pos))

        for vector in ((0, 2, 0), (2, 0, 0), (2, 2, 0), (0, -2, 0), (-2, 0, 0), (-2, -2, 0), (-2, 2, 0), (2, -2, 0), (1, 2, 0), (2, 1, 0), (-1, 2, 0), (2, -1, 0), (1, -2, 0), (-2, 1, 0), (-1, -2, 0), (-2, -1, 0)):
            res = self.game.step_move_to(self, self.pos, vector)
            if res.type == MoveResult.Type.CAPTURE:
                actions.append(Action("capture", *res.pos))

        return actions


    def apply_action(self, action):
            if action.name == "capture":
                self.game.get_piece_at((action.x, action.y, action.z)).die()
            if action.name == "move" or action.name == "move_capture":
                self.pos = action[1:]
