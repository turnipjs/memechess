from .piece import Piece
from .game import Action


class Bishop(Piece):
    def get_actions(self):
        actions = []
        for i in range(1, 19):
            if self.game.is_valid_empty_space((self.x + i, self.y, self.z)):
                actions.append(Action("move", self.x + i, self.y, self.z))
            elif self.game.is_valid_full_enemy_space((self.x + i, self.y, self.z), self.color):
                actions.append(Action("move_capture", self.x + i, self.y, self.z))
                break
            else:
                break

        for i in range(1, 19):
            if self.game.is_valid_empty_space((self.x - i, self.y, self.z)):
                actions.append(Action("move", self.x - i, self.y, self.z))
            elif self.game.is_valid_full_enemy_space((self.x - i, self.y, self.z), self.color):
                actions.append(Action("move_capture", self.x - i, self.y, self.z))
                break
            else:
                break

        for i in range(1, 19):
            if self.game.is_valid_empty_space((self.x, self.y + i, self.z)):
                actions.append(Action("move", self.x, self.y + i, self.z))
            elif self.game.is_valid_full_enemy_space((self.x, self.y + i, self.z), self.color):
                actions.append(Action("move_capture", self.x, self.y + i, self.z))
                break
            else:
                break

        for i in range(1, 19):
            if self.game.is_valid_empty_space((self.x, self.y - i, self.z)):
                actions.append(Action("move", self.x, self.y - i, self.z))
            elif self.game.is_valid_full_enemy_space((self.x, self.y - i, self.z), self.color):
                actions.append(Action("move_capture", self.x, self.y - i, self.z))
                break
            else:
                break

        return actions

    def apply_action(self, action):
        if action.name == "move_capture":
            self.game.get_piece_at((action.x, action.y, action.z)).die()
        if action.name == "move" or action.name == "move_capture":
            self.x = action.x
            self.y = action.y
            self.z = action.z