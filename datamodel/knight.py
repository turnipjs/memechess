from .piece import Piece
from .game import Action, MoveResult

class Knight(Piece):
    def get_actions(self):
        actions = []

        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                res = self.game.step_move_to(self, self.pos, (0, 0, 1))
                if res.type == MoveResult.Type.REGULAR:
                    res = self.game.step_move_to(self, self.pos, (0, 0, 1))

        return actions

    def apply_action(self, action):
        if action.name == "move_capture":
            self.game.get_piece_at((action.x, action.y, action.z)).die()
        if action.name == "move" or action.name == "move_capture":
            self.pos = action[1:]