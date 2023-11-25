import numpy as np
from turtle import pos
from copy import deepcopy


class Character:
    name: str
    color: str
    starting_room: str

    def __init__(self, name:str, color:str, starting_room:str) -> None:
        self.name = name
        self.color = color
        self.starting_room = starting_room


class Room:
    name: str
    position: tuple[int, int]
    adjacent_rooms: list[str] = []
    type: str
    occupants: list[str] = []

    def __init__(self, name, position, adjacent_rooms, type, occupants):
        self.name = name
        self.position = position
        self.adjacent_rooms = adjacent_rooms
        self.type = type
        self.occupants = occupants
        
    def get_adjacent_rooms(self):
        return self.adjacent_rooms
        
    def get_occupied(self):
        return len(self.occupants)>0
        
    def add_occupant(self, player:str):
        self.occupants.add(player)
      
    def remove_occupant(self, player:str):
        if player in self.occupants:
            self.occupants.remove(player)


class Board:

    ROOMS: dict[str, Room] = {
        "Study": Room(
            name = "Study", 
            position = (0,0), 
            adjacent_rooms = ["hallway_0", "Kitchen", "hallway_2"], 
            type = "room",
            occupants = [] 
        ),
        "Hall": Room(
            name = "Hall", 
            position = (0,2),
            adjacent_rooms = ["hallway_0", "hallway_3", "hallway_1"], 
            type = "room",
            occupants = [] 
        ),    
        "Lounge": Room(
            name = "Lounge", 
            position = (0,4),
            adjacent_rooms = ["hallway_1", "Conservatory", "hallway_4"], 
            type = "room",
            occupants = [] 
        ),    
        "Library": Room(
            name = "Library", 
            position = (2,0),
            adjacent_rooms = ["hallway_2", "hallway_5", "hallway_7"], 
            type = "room",
            occupants = [] 
        ),    
        "Billiard Room": Room(
            name = "Billiard Room", 
            position = (2,2),
            adjacent_rooms = ["hallway_3", "hallway_6", "hallway_8", "hallway_5"], 
            type = "room",
            occupants = [] 
        ),        
        "Dining Room": Room(
            name = "Dining Room", 
            position = (2,4),
            adjacent_rooms = ["hallway_4", "hallway_9", "hallway_11"], 
            type = "room",
            occupants = [] 
        ),        
        "Conservatory": Room(
            name = "Conservatory", 
            position = (4,0),
            adjacent_rooms = ["hallway_7", "hallway_10", "Lounge"], 
            type = "room",
            occupants = [] 
        ),        
        "Ballroom": Room(
            name = "Ballroom", 
            position = (4,2),
            adjacent_rooms = ["hallway_8", "hallway_11", "hallway_9", "hallway_10"], 
            type = "room",
            occupants = [] 
        ),        
        "Kitchen": Room(
            name = "Kitchen", 
            position = (4,4),
            adjacent_rooms = ["hallway_10", "hallway_11", "Study"], 
            type = "room",
            occupants = [] 
        ),        
        "hallway_0": Room(
            name = "hallway_0", 
            position = (0,1),
            adjacent_rooms = ["Study", "Hall"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_1": Room(
            name = "hallway_1", 
            position = (0,3),
            adjacent_rooms = ["Hall", "Lounge"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_2": Room(
            name = "hallway_2", 
            position = (1,0),
            adjacent_rooms = ["Study", "Library"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_3": Room(
            name = "hallway_3", 
            position = (1,2),
            adjacent_rooms = ["Hall", "Billiard Room"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_4": Room(
            name = "hallway_4", 
            position = (1,4),
            adjacent_rooms = ["Lounge", "Dining Room"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_5": Room(
            name = "hallway_5", 
            position = (2,1),
            adjacent_rooms = ["Library", "Billiard Room"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_6": Room(
            name = "hallway_6", 
            position = (2,3),
            adjacent_rooms = ["Billiard Room"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_7": Room(
            name = "hallway_7", 
            position = (3,0),
            adjacent_rooms = ["Library", "Conservatory"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_8": Room(
            name = "hallway_8", 
            position = (3,2),
            adjacent_rooms = ["Billiard Room", "Ballroom"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_9": Room(
            name = "hallway_9", 
            position = (3,4),
            adjacent_rooms = ["Dining Room", "Ballroom"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_10": Room(
            name = "hallway_10", 
            position = (4,1),
            adjacent_rooms = ["Conservatory", "Ballroom"], 
            type = "hallway",
            occupants = [] 
        ),        
        "hallway_11": Room(
            name = "hallway_11", 
            position = (4,3),
            adjacent_rooms = ["Ballroom", "Kitchen"], 
            type = "hallway",
            occupants = [] 
        ),        
    }

    CHARACTERS: dict[str, Character] = {
        "Colonel Mustard": Character(name="Colonel Mustard", color="yellow", starting_room="hallway_4"),
        "Miss Scarlet": Character(name="Miss Scarlet", color="red", starting_room="hallway_1"),
        "Professor Plum": Character(name="Professor Plum", color="purple", starting_room="hallway_2"),
        "Mr. Green": Character(name="Mr. Green", color="green", starting_room="hallway_10"),
        "Mrs. White": Character(name="Mrs. White", color="white", starting_room="hallway_11"),
        "Mrs. Peacock": Character(name="Mrs. Peacock", color="blue", starting_room="hallway_7"),
    }

    def __init__(self) -> None:

        self.rooms = deepcopy(self.ROOMS)
        self.player_locations = {}
        self.grid = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ])


    def add_player(self, player:str, character:str):
        starting_room = self.CHARACTERS[character].starting_room
        self.rooms[starting_room].occupants.append(player)
        self.player_locations[player] = starting_room

    def get_location(self, player:str):
        return self.player_locations[player]

    def move_player(self, player:str, room:str):
        ## MOVE PLAYER OUT OF OLD ROOM
        old_room = self.player_locations[player]
        self.rooms[old_room].occupants.remove(player)
        
        ## MOVE PLAYER INTO NEW ROOM
        self.player_locations[player] = room
        self.rooms[room].occupants.append(player)

    def get_adjacent_rooms(self, player):
        ## GET ALL POSSIBLE ADJACENT ROOMS
        adjacent_rooms = []
        current_room = self.get_location(player)
        possible_rooms = self.rooms[current_room].adjacent_rooms

        ## ONLY ADD ROOMS AND UNOCCUPIED HALLWAYS
        for room_name in possible_rooms:
            room = self.rooms[room_name]
            if room.type == "hallway" and room.get_occupied():
                continue
            adjacent_rooms.append(room.name)
        
        return adjacent_rooms
