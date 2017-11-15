import datamodel.game, datamodel.pawn, datamodel.rook, datamodel.knight

g = datamodel.game.Game()
p = datamodel.pawn.Pawn(g, [8, 8, 0], datamodel.game.Color.BLACK)
#b = datamodel.pawn.Pawn(g, [2, 0, 0], datamodel.game.Color.WHITE)
g.add_piece(p)
#g.add_piece(b)

print(p.to_json())

print(g.pieces)
actions = p.get_actions()
print(actions)
#p.apply_action(actions[2])
#print(g.pieces)
