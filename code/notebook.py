class Notebook:
    def __init__(self):
        # Example structure for the notebook
        self.notebook_data = {
            "Me": {"Suspects": set(), "Weapons": set(), "Rooms": set()},
            "Opponent1": {"Suspects": set(), "Weapons": set(), "Rooms": set()},
            # Add more opponents as needed
            "Solution": {"Suspect": None, "Weapon": None, "Room": None},
        }

    def set_cell(self, player, category, item, marking):
        """Sets the marking for a specific cell."""
        if player in self.notebook_data and category in self.notebook_data[player]:
            self.notebook_data[player][category].add((item, marking))
        else:
            print(f"Invalid player or category: {player}, {category}")

    def display_notebook(self):
        """Returns the current state of the notebook."""
        notebook_content = {}
        for player, categories in self.notebook_data.items():
            player_data = {}
            for category, items in categories.items():
                # Check if items is None before iterating
                if items is not None:
                    category_data = [(item, marking) for item, marking in items]
                    player_data[category] = category_data
                else:
                    # If items is None, set an empty list for the category
                    player_data[category] = []
            notebook_content[player] = player_data
        return notebook_content