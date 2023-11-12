class Player:
    def __init__(
        self, 
        player_name:str, 
        character_name:str,
        hand:tuple,
    ):
        self.player_name = player_name  # Player's chosen name for the game
        self.character_name = character_name  # The character chosen to represent the player
        self.hand = hand  # List of cards in player's hand
        self.game_code = None  # Code to join the game session
        self.is_done = False  # Indicates if the player made an incorrect accusation

        assert len(hand) == 3


    def select_character(self, available_characters):
        """Allows the player to select a character from available options."""
        print("Available characters:")
        for character in available_characters:
            print(character)
        choice = input(f"{self.player_name}, please choose your character: ")
        if choice in available_characters:
            self.character_name = choice
            print(f"You have chosen {self.character_name}.")
        else:
            print("Invalid character selection.")

    def enter_game_code(self):
        """Accepts a game code to join the correct game session."""
        self.game_code = input("Enter your game code to join the game: ")
        print(f"Game code {self.game_code} entered.")

    def check_game_code(self, valid_codes):
        """Checks the entered game code against valid codes."""
        if self.game_code in valid_codes:
            print("Game code is valid. Joining the game...")
            return True
        else:
            print("Invalid game code. Please try again.")
            return False

    def confirm_ready(self):
        """Asks the player if they are ready to start the game."""
        ready = input("Are you ready to start the game? (yes/no): ").lower()
        return ready == 'yes'

    def join_game(self, game_roster, player_id):
        """Adds the player to the game roster with their character and player ID."""
        if self.character_name and self.game_code:
            game_roster[self.game_code]['players'][player_id] = self
            print(f"{self.player_name} has joined the game with character {self.character_name}.")

    def setup_initial_state(self, starting_position, initial_cards):
        """Sets up the initial state, including board position and initial cards."""
        self.position = starting_position
        self.hand.extend(initial_cards)
        print(f"{self.player_name} is starting at {self.position} with cards: {self.hand}.")


