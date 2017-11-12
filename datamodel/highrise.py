from .king import King
from .pawn import Pawn
from .piece import Piece
from .game import Action, MoveResult, Game


class Highrise(Piece):
    def __init__(self, game, pos, color):
        Piece.__init__(self, game, pos, color)
        self.levels = 1
    def get_actions(self):
        actions = []

        checkposes = [(self.x + 1, self.y, self.z), (self.x + 1, self.y +1, self.z), (self.x + 1, self.y - 1, self.z),
                      (self.x - 1, self.y, self.z), (self.x - 1, self.y +1, self.z), (self.x - 1, self.y - 1, self.z),
                      (self.x, self.y, self.z), (self.x, self.y + 1, self.z), (self.x, self.y - 1, self.z)]
        for pose in checkposes:
            if self.game.has_piece(pose):
                other_building = self.game.get_piece_at(pose)

                if type(other_building)==Highrise and other_building is not self:
                    actions.append(Action("stack", *pose))
        else:
            for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0), (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
                res = self.game.step_move_to(self, self.pos, vector)
                if res.type == MoveResult.Type.REGULAR:
                    actions.append(Action("move", *res.pos))
                elif res.type == MoveResult.Type.CAPTURE:
                    actions.append(Action("move_capture", *res.pos))

        return actions

    def apply_action(self, action):
        if action.name == "move_capture":
            self.game.get_piece_at((action.x, action.y, action.z)).die()
        if action.name == "stack":
            self.game.get_piece_at((action.x, action.y, action.z)).die()
            self.levels += 1
            print(str(self.levels))
        if action.name == "move" or action.name == "move_capture" or action.name == "stack":
            self.pos = action[1:]

    def get_2nd_text(self): return str(self.levels)