from .piece import Piece
from .pawn import Pawn
from .game import Action, MoveResult

class Knight(Pawn):
    def get_actions(self):
        actions = []
        x = (1, 0, 0)
        y = (0, 1, 0)
        nx = (-1, 0, 0)
        ny = (0, -1, 0)
        horse_movements = [[x, y, y], [y, y, x], [x, x, y], [y, x, x], [x, x, ny], [ny, x, x], [x, ny, ny], [ny, ny, x], [nx, ny, ny], [ny, ny, nx], [nx, nx, ny], [ny, nx, nx], [nx, nx, y], [y, nx, nx], [nx, y, y], [y, nx, nx]]
        for move in horse_movements:
            res = MoveResult(MoveResult.Type.REGULAR, self.pos)
            res = self.game.step_move_to(self, res.pos, (0, 0, 1))
            up_to_3 = 0
            for step in move:
                res = self.game.step_move_to(self, res.pos, step)
                if res.type == MoveResult.Type.INVALID:
                    break
                elif res.type == MoveResult.Type.REGULAR:
                    up_to_3 += 1
                    if res.ends_motion:
                        break

            res = self.game.step_move_to(self, res.pos, (0, 0, -1))
            if up_to_3 == 3:
                if res.type == MoveResult.Type.REGULAR and Action("move", *res.pos) not in actions:
                    actions.append(Action("move", *res.pos))
                elif res.type == MoveResult.Type.CAPTURE and Action("move_capture", *res.pos) not in actions:
                    actions.append(Action("move_capture", *res.pos))

        return actions

    def apply_action(self, action):
        if action.name == "move_capture":
            self.game.get_piece_at((action.x, action.y, action.z)).die()
        if action.name == "move" or action.name == "move_capture":
            self.pos = action[1:]
        
