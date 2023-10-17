import json
from lib2to3.pgen2.pgen import generate_grammar
from flask import Flask, session, request, redirect, url_for, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
from flask_socketio import SocketIO, join_room, leave_room, send
from string import ascii_uppercase
from copy import deepcopy
import random
import sys
import os

# to accommodate this file being run anywhere
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

from board import ROOMS, CHARACTERS, WEAPONS


## FLASK SETUP
app = Flask(__name__)
auth = HTTPBasicAuth()
socketio = SocketIO(app)
app.secret_key = 'your_secret_key_here'


## VARIABLES
games = {}
users = json.load(open("credentials.json"))


def generate_unique_code(length):
    while True:
        game = "".join(random.choices(ascii_uppercase, k=length))
        if game not in games: return game

## Define the verify_password function outside the class
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401
    
##
## WEB PAGES
##
@app.route("/", methods=["POST", "GET"])
@auth.login_required
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name", "")
        code = request.form.get("code", "")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if name == "":
            return render_template("home.html", error="Please enter a name.", code=code, name=name)
        if join != False and code == "":
            return render_template("home.html", error="Please enter a code.", code=code, name=name)
        if create != False:
            code = generate_unique_code(4)
            games[code] = {
                "num_players": 0, 
                "messages": [], 
                "taken_characters": [], 
                "players": {},
                "available_characters": deepcopy(CHARACTERS), 
                "board": deepcopy(ROOMS),
            } #, "board": Board(...)}
            print(games[code]["available_characters"])
        elif join != False and code not in games:
            return render_template("home.html", error="Game does not exist", code=code, name=name)

        session["game"] = code
        session["name"] = name
        return redirect(url_for("character"))

    return render_template('home.html')


@app.route("/character", methods=["POST", "GET"])
@auth.login_required
def character():
    print("\nCHAR\n")
    name = session.get("name", "")
    game = session.get("game", "")
    if request.method == "POST":
        cont = request.form.get("continue", False)
        if cont != False:
            return redirect(url_for("game"))

    if game is None or session.get("game") is None or game not in games:
        return redirect(url_for("home"))
    return render_template("character.html", game=game, name=name, characters=games[game]["available_characters"], taken_characters=games[game]["taken_characters"])


@app.route("/game")
@auth.login_required
def game():
    name = session.get("name")
    game = session.get("game")
    character = games[game]["players"][name]
    if game is None or session.get("game") is None or game not in games:
        return redirect(url_for("home"))
    return render_template("game.html", game=game, character=character, messages=games[game]["messages"])

@app.route("/view_board")
@auth.login_required
def view_board():
    print("HERE")
    game = session.get("game")
    if game is None or game not in games:
        return redirect(url_for("home"))

    center_x, center_y = 2, 2  # Center of the 5x5 board
    board_to_display = {}
    for key, value in ROOMS.items():
        pos_x, pos_y = value.position
        if 0 <= pos_x - center_x < 3 and 0 <= pos_y - center_y < 3:
            board_to_display[key] = value

    return render_template("board.html", board=board_to_display)


## 
## MESSAGING
## 
@socketio.on("connect")
def connect(auth):
    game = session.get("game")
    name = session.get("name")

    if not game or not name: return
    if game not in games: 
        leave_room(game)
        return

    join_room(game)
    send({"name":name, "message": "has entered the game"}, to=game)
    games[game]["num_players"] += 1
    games[game]["players"][name] = None
    print(f"{name} joined game {game}")


@socketio.on("disconnect")
def disconnect():
    game = session.get("game")
    name = session.get("name")
    leave_room(game)
    if game in games and games[game]["num_players"] < 1:
        del games[game]

    send({"name":name, "message": "has left the game"}, to=game)
    print(f"{name} left game {game}")


@socketio.on("message")
def message(data):
    game = session.get("game")
    if game not in games: return

    content = {
        "name": session.get("name"),
        "message": data["data"],
    }
    send(content, to=game)
    games[game]["messages"].append(content)
    print(f"{session.get('name')} said {data['data']}")


@socketio.on("select_character")
def select_character(data):
    name = session.get("name")
    game = session.get("game")
    if game not in games: return

    character = [data["character"]][0]
    games[game]["players"][name] = character
    del games[game]["available_characters"][character]
    content = {
        "name": session.get("name"),
        "character": character,
        "message": f"has chosen {character}"
    }
    games[game]["taken_characters"].append(character)
    session["character"] = character
    send(content, to=game)
    print(f"\n{session.get('name')} selected {character}")
    print(f"Characters Available: {games[game]['available_characters'].keys()}\n")

    return redirect(url_for("view_board"))


if __name__ == '__main__':

    socketio.run(app)
    # socketio.run(app, debug=True)
    # app.run()





# ## export FLASK_APP=clue
# ## export FLASK_ENV=development
# ## flask run --host=0.0.0.0 -p 5001
# ngrok http <port>
