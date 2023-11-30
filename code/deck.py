import random

from board import Board


class Deck:

    def __init__(self) -> None:
        self.weapons = [weapon for weapon in Board.WEAPONS]
        self.characters = [char for char in Board.CHARACTERS]
        self.rooms = [room for room in Board.ROOMS if "Hallway" not in room]


    def draw(self, replace=False):

        room_idx = random.randint(a=0, b=len(self.rooms)-1)
        room = self.rooms[room_idx] if replace else self.rooms.pop(room_idx)

        character_idx = random.randint(a=0, b=len(self.characters)-1)
        character = self.characters[character_idx] if replace else self.characters.pop(character_idx)
            
        weapon_idx = random.randint(a=0, b=len(self.weapons)-1)
        weapon = self.weapons[weapon_idx] if replace else self.weapons.pop(weapon_idx)

        return room, character, weapon


if __name__ == "__main__":

    deck = Deck()
    r,c,w = deck.draw()

    assert len(deck.characters) == 5
    assert len(deck.weapons) == 5
    assert len(deck.rooms) == 8
