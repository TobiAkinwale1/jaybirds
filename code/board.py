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
            adjacent_rooms = ["Hallway 0", "Kitchen", "Hallway 2"], 
            type = "room",
            occupants = [] 
        ),
        "Hall": Room(
            name = "Hall", 
            position = (0,2),
            adjacent_rooms = ["Hallway 0", "Hallway 3", "Hallway 1"], 
            type = "room",
            occupants = [] 
        ),    
        "Lounge": Room(
            name = "Lounge", 
            position = (0,4),
            adjacent_rooms = ["Hallway 1", "Conservatory", "Hallway 4"], 
            type = "room",
            occupants = [] 
        ),    
        "Library": Room(
            name = "Library", 
            position = (2,0),
            adjacent_rooms = ["Hallway 2", "Hallway 5", "Hallway 7"], 
            type = "room",
            occupants = [] 
        ),    
        "Billiard Room": Room(
            name = "Billiard Room", 
            position = (2,2),
            adjacent_rooms = ["Hallway 3", "Hallway 6", "Hallway 8", "Hallway 5"], 
            type = "room",
            occupants = [] 
        ),        
        "Dining Room": Room(
            name = "Dining Room", 
            position = (2,4),
            adjacent_rooms = ["Hallway 4", "Hallway 9", "Hallway 11"], 
            type = "room",
            occupants = [] 
        ),        
        "Conservatory": Room(
            name = "Conservatory", 
            position = (4,0),
            adjacent_rooms = ["Hallway 7", "Hallway 10", "Lounge"], 
            type = "room",
            occupants = [] 
        ),        
        "Ballroom": Room(
            name = "Ballroom", 
            position = (4,2),
            adjacent_rooms = ["Hallway 8", "Hallway 11", "Hallway 10"], 
            type = "room",
            occupants = [] 
        ),        
        "Kitchen": Room(
            name = "Kitchen", 
            position = (4,4),
            adjacent_rooms = ["Hallway 10", "Hallway 11", "Study"], 
            type = "room",
            occupants = [] 
        ),        
        "Hallway 0": Room(
            name = "Hallway 0", 
            position = (0,1),
            adjacent_rooms = ["Study", "Hall"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 1": Room(
            name = "Hallway 1", 
            position = (0,3),
            adjacent_rooms = ["Hall", "Lounge"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 2": Room(
            name = "Hallway 2", 
            position = (1,0),
            adjacent_rooms = ["Study", "Library"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 3": Room(
            name = "Hallway 3", 
            position = (1,2),
            adjacent_rooms = ["Hall", "Billiard Room"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 4": Room(
            name = "Hallway 4", 
            position = (1,4),
            adjacent_rooms = ["Lounge", "Dining Room"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 5": Room(
            name = "Hallway 5", 
            position = (2,1),
            adjacent_rooms = ["Library", "Billiard Room"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 6": Room(
            name = "Hallway 6", 
            position = (2,3),
            adjacent_rooms = ["Billiard Room, Dining Room"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 7": Room(
            name = "Hallway 7", 
            position = (3,0),
            adjacent_rooms = ["Library", "Conservatory"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 8": Room(
            name = "Hallway 8", 
            position = (3,2),
            adjacent_rooms = ["Billiard Room", "Ballroom"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 9": Room(
            name = "Hallway 9", 
            position = (3,4),
            adjacent_rooms = ["Dining Room", "Ballroom"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 10": Room(
            name = "Hallway 10", 
            position = (4,1),
            adjacent_rooms = ["Conservatory", "Ballroom"], 
            type = "Hallway",
            occupants = [] 
        ),        
        "Hallway 11": Room(
            name = "Hallway 11", 
            position = (4,3),
            adjacent_rooms = ["Ballroom", "Kitchen"], 
            type = "Hallway",
            occupants = [] 
        ),        
    }

    CHARACTERS: dict[str, Character] = {
        "Colonel Mustard": Character(name="Colonel Mustard", color="yellow", starting_room="Hallway 4"),
        "Miss Scarlet": Character(name="Miss Scarlet", color="red", starting_room="Hallway 1"),
        "Professor Plum": Character(name="Professor Plum", color="purple", starting_room="Hallway 2"),
        "Mr. Green": Character(name="Mr. Green", color="green", starting_room="Hallway 10"),
        "Mrs. White": Character(name="Mrs. White", color="white", starting_room="Hallway 11"),
        "Mrs. Peacock": Character(name="Mrs. Peacock", color="blue", starting_room="Hallway 7"),
    }

    WEAPONS: list[str] = [
        "Rope",
        "Lead Pipe",
        "Knife",
        "Wrench",
        "Candlestick",
        "Revolver",        
    ]

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
            if room.type == "Hallway" and room.get_occupied():
                continue
            adjacent_rooms.append(room.name)
        
        return adjacent_rooms
