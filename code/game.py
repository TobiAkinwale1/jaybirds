from copy import deepcopy
from xml.dom import NotFoundErr

from player import Player
from board import Board, Character
from deck import Deck


class Game:

    games = {}

    def __init__(self, code:str) -> None:
        
        assert len(code) == 4
        Game.games[code] = self

        ## REFERENCES
        self.board = Board()
        self.deck = Deck()

        ## ATTRIBUTES
        self.code = code
        self.turn = None
        self.messages = []
        self.players = {}
        self.messages = []
        self.rebuttals = []
        self.solution = self.deck.draw(replace=False)
        self.available_characters = deepcopy(Board.CHARACTERS)

        ## Internal variables for stepping turn
        self._player_list = []
        self._turn_idx = 0

    def get_board(self):
        return self.board

    def get_player(self, name):
        assert name in self.players, f"Invalid player name {name}"
        return self.players[name]

    def add_player(self, name:str, char:str):
        self.board.add_character(char)        
        self.players[name] = Player(
            player_name=name,
            character_name=char,
        )
        self._player_list.append(self.players[name])

    def get_messages(self):
        return self.messages

    def add_message(self, message):
        self.messages.append(message)

    def step_turn(self):
        ## START GAME
        if self._turn_idx == 0:
            for i,player in enumerate(self.players.values()):
                hand = self.deck.deal(num_players=len(self.players)-i)
                player.set_hand(hand)
        ## NEXT TURN
        self.turn = self.player_list[self._turn_idx % len(self.player_list)]
        self._turn_idx += 1
        self.reset_rebuttals()
        return self.turn.player_name

    def step_rebuttals(self):
        print(f"STEP REBUTTALS {self.rebuttals}")
        return self.rebuttals.pop(0)

    def reset_rebuttals(self):
        self.rebuttals = list(self.players.keys())
        self.rebuttals.remove(self.turn.player_name)
        print(f"RESET REBUTTALS {self.rebuttals}")

    def check_solution(self, room:str, character:str, weapon:str):
        return (room, character, weapon) == self.solution

    def end_game(self, name):
        print(f"{name} solved the case!")
        print(f"They discovered that {self.solution[1]} commited the murder in the {self.solution[0]} with a {self.solution[2]}")
    
    @classmethod
    def del_game(cls, code:str):
        del cls.games[code]

    def get_available_characters(self):
        return self.available_characters

    def remove_available_character(self, character):
        del self.available_characters[character]

    @classmethod
    def lookup(cls, code:str):
        # assert code in cls.games, f"Invalid game code {code}"
        return cls.games.get(code, None)

    @classmethod
    def create(cls, code:str):
        # assert code in cls.games, f"Invalid game code {code}"
        cls.games[code] = cls(code=code)

    @property
    def player_list(self):
        if self._player_list is None:
            self._player_list = list(self.players.items())
        return self._player_list


if __name__ == "__main__":

    game = Game("ABCD")
    Game.set_player("ABCD", "grey", "Colonel Mustard")
    Game.set_player("ABCD", "amda", "Miss Scarlet")
    Game.set_player("ABCD", "tobi", "Professor Plum")
    Game.set_player("ABCD", "shrn", "Mr. Green")