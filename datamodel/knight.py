from .piece import Piece
from .game import Action


class Knight(Piece):
    def get_actions(self):
        actions = []

        if self.game.is_valid_empty_space((self.x + 1, self.y - 2, self.z)):
            actions.append(Action("move", self.x + 1, self.y - 2 , self.z))
        if self.game.is_valid_full_enemy_space((self.x + 1, self.y - 2, self.z), self.color):
            actions.append(Action("move_capture", self.x + 1, self.y - 2))

        if self.game.is_valid_empty_space((self.x + 2, self.y - 1, self.z)):
            actions.append(Action("move", self.x + 2, self.y - 1, self.z))
        if self.game.is_valid_full_enemy_space((self.x + 2, self.y - 1, self.z), self.color):
            actions.append(Action("move_capture", self.x +2, self.y - 1))



        return actions

    def apply_action(self, action):
        if action.name == "move_capture":
            self.game.get_piece_at((action.x, action.y, action.z)).die()
        if action.name == "move" or action.name == "move_capture":
            self.x = action.x
            self.y = action.y
            self.z = action.z