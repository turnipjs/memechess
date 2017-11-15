from flask import Flask, send_from_directory, send_file, redirect, request, jsonify
from datamodel import game
from flask_socketio import SocketIO, emit, join_room
import eventlet
import create_game

eventlet.monkey_patch()

class Session:
	def __init__(self, game_id):
		self.game_id = game_id
		self.board = create_game.create()
		self.board.start_turn(game.Color.WHITE)
		self.room = "room_"+str(game_id)
		self.black_joined = False
		self.white_joined = False
		self.player_turn = game.Color.WHITE

app = Flask(__name__)
socketio = SocketIO(app)

sessions = {}

@app.route('/f/<path:path>')
def send_assets(path):
	return send_from_directory('ws_frontend', path)

@app.route('/i/<path:path>')
def send_images(path):
	return send_from_directory('public/img', path)

@app.route("/play/<int:game_id>/<color>")
def handle_play(game_id, color):
	return send_file("ws_frontend/index.html")

# @app.route("/api/get_board_state/<int:game_id>")
# def get_board_state(game_id):
# 	return jsonify(board.to_json())

# @app.route("/api/apply_action/<int:game_id>/<int:px>/<int:py>/<int:pz>/<name>/<int:x>/<int:y>/<int:z>")
# def apply_action(game_id, px, py, pz, name, x, y, z):
# 	board.get_piece_at((px, py, pz)).apply_action(game.Action(name, x, y, z))
# 	return jsonify(board.to_json())

@socketio.on('client_start')
def client_start(message):
	gid = message['game_id']
	if gid not in sessions:
		sessions[gid] = Session(gid)
	session = sessions[gid]
	join_room(session.room)
	emit('update_board', session.board.to_json(), room=session.room)
	if message['color']=="WHITE":
		session.white_joined=True
	elif message['color']=="BLACK":
		session.black_joined=True
	if session.white_joined and session.black_joined:
		emit('start_turn', {"color": "WHITE"}, room=session.room)

@socketio.on('send_action')
def send_action(message):
	session = sessions[message['game_id']]
	session.board.get_piece_at(message["piece"]).apply_action(game.Action(message["name"], *message["pos"]))
	session.player_turn = session.player_turn.opposite()
	session.board.start_turn(session.player_turn)
	emit('start_turn', {"color": session.player_turn.to_json_string()}, room=session.room)
	emit('update_board', session.board.to_json(), room=session.room)

@app.route('/')
def handle_root():
	return redirect('play/1/white')

if __name__=="__main__":
	socketio.run(app)