from .piece import Piece
from .game import Action, MoveResult

class Mage(Piece):
    def __init__(self, game, pos, color):
        Piece.__init__(self, game, pos, color)
        self.attacking = None

    def _get_actions(self):
       actions = []

       #for dropping a levitated piece
       if self.attacking != None:
                    actions.append(Action("unlevitate", self.attacking.x, self.attacking.y, self.attacking.z))

       #for moving
       for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0),
                      (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
           res = self.game.step_move_to(self, self.pos, vector)
           if res.type == MoveResult.Type.REGULAR:
               actions.append(Action("move", *res.pos))

       #for levitating a piece
       if self.attacking == None:
            for vector in ((0, 1, 0), (1, 0, 0), (1, 1, 0), (0, -1, 0), (-1, 0, 0),
                          (-1, -1, 0), (1, -1, 0), (-1, 1, 0)):
                res = self.game.step_move_to(self, self.pos, vector)
                if res.type == MoveResult.Type.CAPTURE:
                    actions.append(Action("levitate", *res.pos))

       """#for moving the levitated piece
       if self.attacking != None:
            for vector in ((0, 1, 1), (1, 0, 1), (1, 1, 1), (0, -1, 1), (-1, 0, 1),
                      (-1, -1, 1), (1, -1, 1), (-1, 1, 1)):
               res = self.game.step_move_to(self, self.pos, vector)
               if res.type != res.type == MoveResult.Type.CAPTURE:
                   actions.append(Action("move_levitated", *res.pos))"""

       return actions

#Will need to be changed to account for unliftable pieces?


    def apply_action(self, action):
       if action.name == "move":
           self.pos = action[1:]
       if action.name == "move_levitated":
           self.attacking.pos = action[1:]
       if action.name == "levitate":
           self.game.get_piece_at((action.x, action.y, action.z)).frozen=True
           self.attacking = self.game.get_piece_at(action[1:])
           self.game.get_piece_at((action.x, action.y, action.z)).z+=1
       if action.name == "unlevitate" and self.game.get_piece_at((action.x, action.y, action.z)).frozen==True:
           if self.game.is_valid_empty_space((action.x, action.y, action.z-1))==True:
                self.attacking = None
                self.game.get_piece_at((action.x, action.y, action.z)).frozen=False
                self.game.get_piece_at((action.x, action.y, action.z)).z-=1
           elif self.game.get_piece_at((action.x, action.y, action.z-1)).can_be_captured==True:
                self.game.get_piece_at((action.x, action.y, action.z - 1)).die()
                self.attacking = None
                self.game.get_piece_at((action.x, action.y, action.z)).frozen = False
                self.game.get_piece_at((action.x, action.y, action.z)).z -= 1
