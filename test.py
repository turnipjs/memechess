import datamodel.game, datamodel.pawn

g = datamodel.game.Game()
p = datamodel.pawn.Pawn(g, [0, 0, 0], datamodel.game.Color.WHITE)
g.add_piece(p)
print(g.get_piece_at([0, 0, 0]))

actions = p.get_actions()
print(actions)
p.apply_action(actions[0])
print(p)