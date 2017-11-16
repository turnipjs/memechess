from .king import King
from .game import Action, MoveResult, Game


class Wall(King):
    identifier = "wall"
    
    def __init__(self, game, pos, color):
        King.__init__(self, game, pos, color)
        self.health = 1
    def _get_actions(self):
        actions = []

        for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0), (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
            res = self.game.step_move_to(self, self.pos, vector)
            if res.type == MoveResult.Type.REGULAR:
                actions.append(Action("move", *res.pos))
            elif res.type == MoveResult.Type.CAPTURE:
                actions.append(Action("move_capture", *res.pos))

        return actions

class NoMoveWall(Wall):
    identifier = "wall"
    can_be_captured = False

    def _get_actions(self):
        return []