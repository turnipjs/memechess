from flask import Flask, send_from_directory, send_file, redirect, request, jsonify
from datamodel import game
import create_game

board = create_game.create()

app = Flask(__name__)

@app.route('/f/<path:path>')
def send_assets(path):
	return send_from_directory('ws_frontend', path)

@app.route('/i/<path:path>')
def send_images(path):
	return send_from_directory('public/img', path)

@app.route("/play/<int:game_id>/<color>")
def handle_play(game_id, color):
	return send_file("ws_frontend/index.html")

@app.route("/api/get_board_state/<int:game_id>")
def get_board_state(game_id):
	return jsonify(board.to_json())

@app.route("/api/apply_action/<int:game_id>/<int:px>/<int:py>/<int:pz>/<name>/<int:x>/<int:y>/<int:z>")
def apply_action(game_id, px, py, pz, name, x, y, z):
	board.get_piece_at((px, py, pz)).apply_action(game.Action(name, x, y, z))
	return jsonify(board.to_json())

@app.route('/')
def handle_root():
	return redirect('play/1/white')

if __name__=="__main__":
	app.run(debug=True)