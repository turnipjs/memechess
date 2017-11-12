import datamodel.game, datamodel.pawn, datamodel.rook

g = datamodel.game.Game()
p = datamodel.rook.Rook(g, [8, 8, 0], datamodel.game.Color.BLACK)
#b = datamodel.pawn.Pawn(g, [2, 0, 0], datamodel.game.Color.WHITE)
g.add_piece(p)
#g.add_piece(b)

print(g.pieces)
actions = p.get_actions()
print(actions)
#p.apply_action(actions[2])
print(g.pieces)