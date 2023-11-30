import json
# from lib2to3.pgen2.pgen import generate_grammar
from flask import Flask, session, request, redirect, url_for, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
from flask_socketio import SocketIO, join_room, leave_room, send
from string import ascii_uppercase
import random
import sys
import os

# to accommodate this file being run anywhere
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

from board import Board
from game import Game


## FLASK SETUP
app = Flask(__name__)
auth = HTTPBasicAuth()
socketio = SocketIO(app)
app.secret_key = 'your_secret_key_here'


## VARIABLES
users = json.load(open("credentials.json"))
debug = True

## GENERATE GAME CODES
def generate_unique_code(length):
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))
        if Game.lookup(code) is None: return code

## AUTHENTICATE USERNAME AND PASSWORD
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

## THROW ERROR FOR INCORRECT USER CREDENTIALS
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401
    

###############
## WEB PAGES ##
###############

## HOME PAGE
@app.route("/", methods=["POST", "GET"])
@auth.login_required
def home():
    session.clear()
    if request.method == "POST":
        ## PULL DATA FROM HTML FORM
        name = request.form.get("name", "")
        code = request.form.get("code", "")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        ## WARN USER IF JOINING/CREATING A GAME WITHOUT ENTERING A NAME
        if name == "":
            return render_template("home.html", error="Please enter a name.", code=code, name=name)
        ## WARN USER IF TRYING TO JOIN A GAME WITHOUT ENTERING A CODE
        if join != False and code == "":
            return render_template("home.html", error="Please enter a code.", code=code, name=name)
        ## GENERATE A NEW GAME 
        if create != False:
            code = generate_unique_code(4)
            Game.create(code=code)
        ## WARN USER TRYING TO JOIN A NON-EXISTANT GAME
        elif join != False and Game.lookup(code) is None:
            print("\nGAME DOES NOT EXIST\n")
            return render_template("home.html", error="Game does not exist", code=code, name=name)

        ## ADD USER NAME AND GAME CODE TO THE SESSION DICT (CLIENT SIDE)
        session["game_code"] = code
        session["name"] = name
        return redirect(url_for("character"))
    ## RENDER THE HOME PAGE
    return render_template('home.html')


## CHARACTER SELECTION PAGE
@app.route("/character", methods=["POST", "GET"])
@auth.login_required
def character():
    ## PULL DATA FROM SESSION DICT
    name = session.get("name", "")
    game_code = session.get("game_code", "")
    game_instance = Game.lookup(game_code)

    ## DEBUG STATEMENTS
    if debug: print(f"\nCHAR SESSION {session}\n")

    ## REDIRECT TO THE GAME PAGE WHEN THE USER HITS CONTINUE
    if request.method == "POST":
        cont = request.form.get("continue", False)
        if cont != False:
            return redirect(url_for("game"))

    ## REDIRECT HOME IF USER TRIES JOINING A GAME THAT DOESN'T EXIST
    if game_code is None or session.get("game_code") is None or game_instance is None:
        return redirect(url_for("home"))

    ## RENDER THE SELECTION PAGE
    return render_template("character.html", game=game_code, name=name, characters=game_instance.get_available_characters())
    # return render_template("character.html", game=game_code, name=name, characters=games[game_code]["available_characters"], taken_characters=games[game_code]["taken_characters"])


## GAME BOARD PAGE
@app.route("/game")
@auth.login_required
def game():
    ## PULL DATA FROM SESSION DICT
    name = session.get("name")
    game_code = session.get("game_code")
    game_instance = Game.lookup(game_code)
    
    ## REDIRECT HOME IF USER TRIES JOINING A GAME THAT DOESN'T EXIST
    if game_code is None or session.get("game_code") is None or game_instance is None:
        return redirect(url_for("home"))
    
    ## DEBUG STATEMENTS
    if debug: 
        print(f"\nGAME SESSION {session}\n")
        print(f"\nSERVE GAME PAGE {name}\n")
        print(game_instance.players)
    
    ## GET AVAILABLE MOVES
    adjacent_rooms = game_instance.board.get_adjacent_rooms(name)

    ## RENDER THE GAME PAGE
    character = game_instance.get_player(name).character_name
    return render_template(
        "game.html", 
        game=game_code, 
        player=name, 
        character=character, 
        messages=game_instance.get_messages(), 
        board=game_instance.board.rooms, 
        hand=game_instance.players[name].hand, 
        adjacent_rooms=adjacent_rooms,
        characters=game_instance.board.CHARACTERS,
        weapons=game_instance.board.WEAPONS,
    )

    # ## RENDER THE GAME PAGE
    # return render_template("game.html", game=game_code, character=game_instance.players[name].playerName, messages=game_instance.messages, board=game_instance.board.ROOMS, hand=game_instance.players[name].hand)

#########################
## MESSAGING FUNCTIONS ##
#########################

## CONNECTS TO A GAME ROOM
@socketio.on("connect")
def connect(auth):
    ## PULL DATA FROM SESSION DICT
    name = session.get("name")
    game_code = session.get("game_code")
    game = Game.lookup(game_code)

    ## HANDLE INVALID GAME CODES
    if not game_code or not name: 
        return
    if game is None: 
        leave_room(game_code)
        return
    
    ## DEBUG STATEMENTS
    if debug: print(f"\nCONNECT SESSION {session}\n")

    ## ADD USER TO GAME AND SEND MESSAGE TO PLAYERS
    join_room(game_code)
    # send({"name":name, "message": "has entered the game"}, to=game_code)
    ## UPDATE GAME DICT WITH PLAYER INFO
    # games[game_code]["num_players"] += 1
    # games[game_code]["players"][name] = None
    # print(f"{name} joined game {game_code}")

## LEAVES A GAME ROOM
@socketio.on("disconnect")
def disconnect():
    ## PULL DATA FROM SESSION DICT
    # name = session.get("name")
    game_code = session.get("game_code")
    # game_instance = Game.lookup(game_code)
    leave_room(game_code)
    
    ## DEBUG STATEMENTS
    if debug: print(f"\nDISCONNECT SESSION {session}\n")

    # ## REMOVE GAME IF ALL PLAYERS LEAVE
    # if game_code in games and games[game_code]["num_players"] < 1:
    #     del games[game_code]

    # # SEND MESSAGE TO GAME LOBBY WHEN A USER LEAVES
    # send({"name":name, "message": "has left the game"}, to=game_code)
    # print(f"{name} left game {game_code}")


## SEND A MESSAGE TO ALL USERS
@socketio.on("message")
def message(data):
    ## PULL GAME CODE FROM SESSION DICT
    game_code = session.get("game_code")
    game = Game.lookup(game_code)
    if game is None: return
    
    ## DEBUG STATEMENTS
    if debug: print(f"\nMESSAGE SESSION {session}\n")
    
    ## BUILD MESSAGE FROM ARGUMENTS
    content = {
        "name": session.get("name"),
        "type": "chat",
        "message": data["data"],
    }
    ## SEND MESSAGE TO ALL USERS IN THE GAME LOBBY
    send(content, to=game_code)
    game.add_message(content)
    print(f"{session.get('name')} said {data['data']}")


## RECEIVE CHARACTER SELECTION FROM CLIENT
@socketio.on("select_character")
def select_character(data):
    ## PULL DATA FROM SESSION DICT
    name = session.get("name")
    game_code = session.get("game_code")
    game = Game.lookup(game_code)
    if game is None: return
    
    ## UPDATE GAME DATA WITH SELECTED CHARACTER
    character = [data["character"]][0]
    session["character"] = character

    ## DEBUG STATEMENTS
    if debug: 
        print(f"\nSELECT CHAR SESSION {session}\n")
        print(f"\nCHARACTER SELECTED {name}\n")
        print(game.players)

    ## UPDATE GAME PLAYER ATTRIBUTES
    game.add_player(name, character)
    game.remove_available_character(character)

    ## BUILD CHARACTER SELECTION MESSAGE
    content = {
        "name": "Server",
        "type": "chat",
        "character": character,
        "message": f"{name} chose {character}"
    }
    ## SEND CHARACTER SELECTION MESSAGE TO PLAYERS
    send(content, to=game_code)
    socketio.emit("character_selected", room=request.sid)

    ## SEND SPAWN MESSAGE
    room = game.board.get_location(name)
    content = {
        "name": name,
        "type": "move",
        "old_room": room,
        "new_room": room,
        "message": f"{name} joined in {room}",
    }
    ## SEND MOVE MESSAGE
    game.add_message(content)
    send(content, to=game_code)


## RECEIVE GAME START FROM CLIENT
@socketio.on("startGame")
def start_game(data):
    ## PULL GAME CODE FROM SESSION DICT
    name = session.get('name')
    game_code = session.get("game_code")
    game = Game.lookup(game_code)
    if game is None: return
    
    ## STEP GAME
    player = game.step_turn()
    comm_turn(player)

    ## DEBUG STATEMENTS
    if debug: 
        print(f"\nSTART SESSION {session}\n")
        print(f"\nCHARACTER SELECTED {name}\n")
        print(game.turn)

    ## BUILD MESSAGE FROM ARGUMENTS
    content = {
        "name": "Server",
        "type": "start",
        "message": f"{player}'s Turn!",
    }
    ## SEND MESSAGE TO ALL USERS IN THE GAME LOBBY
    send(content, to=game_code)
    game.add_message(content)
    if debug: print(f"{name} said {data['data']}")


## SEND A TURN TO ALL USERS
def comm_turn(player:str):
    ## PULL GAME CODE FROM SESSION DICT
    game_code = session.get("game_code")
    game = Game.lookup(game_code)
    if game is None: return
    
    ## BUILD MESSAGE FROM ARGUMENTS
    content = {
        "name": player,
    }
    ## SEND MESSAGE TO ALL USERS IN THE GAME LOBBY
    send(content, to=game_code)
    game.add_message(content)


## RECEIVE MOVE FROM CLIENT
@socketio.on("submitMove")
def submit_move(data):
    ## PULL GAME CODE FROM SESSION DICT
    name = session.get("name")
    game_code = session.get("game_code")
    game = Game.lookup(game_code)
    if game is None: return
    
    ## DEBUG STATEMENTS
    if debug: print(f"\nMESSAGE SESSION {session}\n")

    ## MOVE PLAYER
    old_room = game.board.get_location(name)
    game.board.move_player(name, data['room'])

    ## BUILD MESSAGE FROM ARGUMENTS
    content = {
        "name": name,
        "type": "move",
        "old_room": old_room,
        "new_room": data['room'],
        "message": f"{name} moved to the {data['room']}",
    }

    ## SEND MESSAGE TO ALL USERS IN THE GAME LOBBY
    game.add_message(content)
    send(content, to=game_code)
    if debug: print(f"{session.get('name')} moved to the {data['room']}")


## RECEIVE SUGGESTION FROM CLIENT
@socketio.on("submitSuggestion")
def submit_suggestion(data):
    ## PULL GAME CODE FROM SESSION DICT
    name = session.get("name")
    game_code = session.get("game_code")
    game = Game.lookup(game_code)
    if game is None: return
    
    ## DEBUG STATEMENTS
    if debug: print(f"\nMESSAGE SESSION {session}\n")

    ## MOVE PLAYER
    player = data['player']
    room = data['room']
    character = data['character']
    weapon = data['weapon']

    ## MOVE PLAYER WHOSE CHAR WAS SUGGESTED
    suggested_player = [player.player_name for player in game.players.values() if player.character_name == character][0]
    old_room = game.board.get_location(suggested_player)
    game.board.move_player(suggested_player, room)
    
    ## SEND MOVE MESSAGE
    content = {
        "name": suggested_player,
        "type": "move",
        "old_room": old_room,
        "new_room": room,
        "message": f"{suggested_player} was moved to the {room}",
    }    
    ## SEND MOVE MESSAGE
    game.add_message(content)
    send(content, to=game_code)
    if debug: print(content["message"])

    ## SEND SUGGESTION MESSAGE
    content = {
        "name": name,
        "type": "suggest",
        "player": player,
        "room": room,
        "character": character,
        "weapon": weapon,
        "message": f"{player} suggested it was {character} in the {room} with a {weapon}",
    }

    ## SEND MESSAGE TO ALL USERS IN THE GAME LOBBY
    game.add_message(content)
    send(content, to=game_code)
    if debug: print(content["message"])



## LOOP
## submitMove -> 
## promptSuggestion -> 
## submitSuggestion -> 
## promptRebuttal -> 
## submitRebuttal -> 
## promptEndTurn -> 
## submitEndTurn -> 
## stepTurn -> 




if __name__ == '__main__':

    socketio.run(app)
    # socketio.run(app, debug=True)
    # app.run()




'''
export FLASK_APP=clue
export FLASK_ENV=development
flask run --host=0.0.0.0 -p 5001
ngrok http <port>
'''