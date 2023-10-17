from turtle import pos
import numpy as np

class Character:
    name: str
    color: str

    def __init__(self, name, color):
        self.name = name
        self.color = color

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

CHARACTERS: dict[str, Character] = {
    "Colonel Mustard": Character(name="Colonel Mustard", color="yellow"),
    "Miss Scarlet": Character(name="Miss Scarlet", color="red"),
    "Professor Plum": Character(name="Professor Plum", color="purple"),
    "Mr. Green": Character(name="Mr. Green", color="green"),
    "Mrs. White": Character(name="Mrs. White", color="white"),
    "Mrs. Peacock": Character(name="Mrs. Peacock", color="blue"),
}

WEAPONS = [
    "Rope",
    "Lead Pipe",
    "Knife",
    "Wrench",
    "Candlestick",
    "Revolver",
]

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
        type = "hallway",
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
        name = "Room", 
        position = (2,2),
        adjacent_rooms = ["", "", ""], 
        type = "room",
        occupants = [] 
    ),        
    "Dining Room": Room(
        name = "Room", 
        position = (2,4),
        adjacent_rooms = ["", "", ""], 
        type = "room",
        occupants = [] 
    ),        
    "Conservatory": Room(
        name = "Conservatory", 
        position = (4,0),
        adjacent_rooms = ["", "", ""], 
        type = "room",
        occupants = [] 
    ),        
    "Ballroom": Room(
        name = "Ballroom", 
        position = (4,2),
        adjacent_rooms = ["", "", ""], 
        type = "room",
        occupants = [] 
    ),        
    "Kitchen": Room(
        name = "Kitchen", 
        position = (4,4),
        adjacent_rooms = ["", "", ""], 
        type = "room",
        occupants = [] 
    ),        
    "hallway_0": Room(
        name = "hallway_0", 
        position = (0,1),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_1": Room(
        name = "hallway_1", 
        position = (0,3),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_2": Room(
        name = "hallway_2", 
        position = (1,0),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_3": Room(
        name = "hallway_3", 
        position = (1,2),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_4": Room(
        name = "hallway_4", 
        position = (1,4),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_5": Room(
        name = "hallway_5", 
        position = (2,1),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_6": Room(
        name = "hallway_6", 
        position = (2,3),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_7": Room(
        name = "hallway_7", 
        position = (3,0),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_8": Room(
        name = "hallway_8", 
        position = (3,2),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_9": Room(
        name = "hallway_9", 
        position = (3,4),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_10": Room(
        name = "hallway_10", 
        position = (4,1),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
    "hallway_11": Room(
        name = "hallway_11", 
        position = (4,3),
        adjacent_rooms = ["", "", ""], 
        type = "hallway",
        occupants = [] 
    ),        
}

class Board:
    def __init__(self, characters) -> None:
        self.occupied_spaces = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ])

        # for room in self.ROOMS


        # valid_spaces = np.array([
        #     [1, 1, 1, 1, 1],
        #     [1, 0, 1, 0, 1],
        #     [1, 1, 1, 1, 1],
        #     [1, 0, 1, 0, 1],
        #     [1, 1, 1, 1, 1],
        # ])
        # occupied_spaces = np.array([
        #     ["", "", "", "Miss Scarlet", ""],
        #     ["Professor Plum", "", "", "", "Colonel Mustard"],
        #     ["", "", "", "", ""],
        #     ["Mrs. Peacock", "", "", "", ""],
        #     ["", "Mr. Green", "", "Mrs. White", ""],
        # ])

        # rooms = [
        #     ["Study", 1, "Hall", 1, "Lounge"],
        #     [1, 0, 1, 0, 1],
        #     ["Library", 1, "Billiard Room", 1, "Dining Room"],
        #     [1, 0, 1, 0, 1],
        #     ["Conservatory", 1, "Ballroom", 1, "Kitchen"],
        # ]

    # def update(self, )
