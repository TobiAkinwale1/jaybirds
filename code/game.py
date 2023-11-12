

from xml.dom import NotFoundErr
from player import Player
from board import Board
from deck import Deck


class Game:

    games = {}

    def __init__(self, code:str) -> None:
        
        assert len(code) == 4
        Game.games[code] = self

        ## REFERENCES
        # self.board = Board()
        self.deck = Deck()

        ## ATTRIBUTES
        self.code = code
        self.turn = None
        self.players = {}
        self.solution = self.deck.draw(replace=False)

        ## Internal variables for stepping turn
        self._player_list = None
        self._turn_idx = 0

    def get_board(self):
        return self.board

    def get_player(self, name):
        assert name in self.players, f"Invalid player name {name}"
        return self.players[name]

    def step_turn(self):
        self.turn = self.player_list[self._turn_idx % len(self.player_list)]
        self._turn_idx += 1

    def check_solution(self, room:str, character:str, weapon:str):
        return (room, character, weapon) == self.solution

    def end_game(self, name):
        print(f"{name} solved the case!")
        print(f"They discovered that {self.solution[1]} commited the murder in the {self.solution[0]} with a {self.solution[2]}")


    @classmethod
    def set_player(cls, code:str, name:str, char:str):
        game = cls.lookup(code)
        hand = game.deck.draw(replace=False)
        game.players[name] =  Player(
            playerName=name,
            characterName=char,
            hand=hand
        )

    @classmethod
    def lookup(cls, code:str):
        assert code in cls.games, f"Invalid game code {code}"
        return cls.games[code]

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