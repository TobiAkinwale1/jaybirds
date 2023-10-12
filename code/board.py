from turtle import pos
import numpy as np


CHARACTERS = {
    "Colonel Mustard": "yellow",
    "Miss Scarlet": "red",
    "Professor Plum": "purple",
    "Mr. Green": "green",
    "Mrs. White": "white",
    "Mrs. Peacock": "blue",
}

WEAPONS = [
    "Rope",
    "Lead Pipe",
    "Knife",
    "Wrench",
    "Candlestick",
    "Revolver",
]

ROOMS = {
    "Study": { 
        "position": (0,0), 
        "adjacent_rooms": ["hallway_0", "Kitchen", "hallway_2"], 
        "type": "room",
        "occupants":[] 
    },
    "Hall": { 
        "position": (0,2),
        "adjacent_rooms": ["hallway_0", "hallway_3", "hallway_1"], 
        "type": "hallway",
        "occupants":[] 
    },    
    "Lounge": { 
        "position": (0,4),
        "adjacent_rooms": ["hallway_1", "Conservatory", "hallway_4"], 
        "type": "room",
        "occupants":[] 
    },    
    "Library": { 
        "position": (2,0),
        "adjacent_rooms": ["hallway_2", "hallway_5", "hallway_7"], 
        "type": "room",
        "occupants":[] 
    },    
    "Billiard Room": { 
        "position": (2,2),
        "adjacent_rooms": ["", "", ""], 
        "type": "room",
        "occupants":[] 
    },        
    "Dining Room": { 
        "position": (2,4),
        "adjacent_rooms": ["", "", ""], 
        "type": "room",
        "occupants":[] 
    },        
    "Conservatory": { 
        "position": (4,0),
        "adjacent_rooms": ["", "", ""], 
        "type": "room",
        "occupants":[] 
    },        
    "Ballroom": { 
        "position": (4,2),
        "adjacent_rooms": ["", "", ""], 
        "type": "room",
        "occupants":[] 
    },        
    "Kitchen": { 
        "position": (4,4),
        "adjacent_rooms": ["", "", ""], 
        "type": "room",
        "occupants":[] 
    },        
    "hallway_0": { 
        "position": (0,1),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_1": { 
        "position": (0,3),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_2": { 
        "position": (1,0),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_3": { 
        "position": (1,2),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_4": { 
        "position": (1,4),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_5": { 
        "position": (2,1),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_6": { 
        "position": (2,3),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_7": { 
        "position": (3,0),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_8": { 
        "position": (3,2),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_9": { 
        "position": (3,4),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_10": { 
        "position": (4,1),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
    "hallway_11": { 
        "position": (4,3),
        "adjacent_rooms": ["", "", ""], 
        "type": "hallway",
        "occupants":[] 
    },        
}


# class Room:

#     def __init__(self, name, adjacent_rooms:list) -> None:
#         self.name = name
#         self.position = Board.ROOMS[name]
#         self.adjacent_rooms = adjacent_rooms

# Conservatory = Room(
#     name="Conservatory"
# )


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
