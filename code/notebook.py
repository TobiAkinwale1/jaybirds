from board import Board

class Notebook:
    def __init__(self, player_name):
        # Example structure for the notebook

        self.notebook_data = {}

        self.notebook_data[player_name] = {
            'Suspects': {sus: None for sus in Board.CHARACTERS},
            'Weapons': {wep: None for wep in Board.WEAPONS},
            'Rooms': {room: None for room in Board.ROOMS if ('Hallway' not in room)}
        }

    def add_player(self, player_name):
        self.notebook_data[player_name] = {
            'Suspects': {sus: None for sus in Board.CHARACTERS},
            'Weapons': {wep: None for wep in Board.WEAPONS},
            'Rooms': {room: None for room in Board.ROOMS if ('Hallway' not in room)}
        }

    def set_cell(self, player, category, item, marking):
        '''Sets the marking for a specific cell.'''
        if (player in self.notebook_data) and (category in self.notebook_data[player]) and (item in self.notebook_data[player][category]):
            self.notebook_data[player][category][item] = marking
        else:
            print(f'Invalid entry: {player}, {category}, {item}')

    def get_table(self):
        table = {}

        for player_name, player in self.notebook_data.items():
            for category_name, category in self.notebook_data[player_name].items():
                if (category_name not in table.keys()):
                    table[category_name] = {}

                for item_name, item in self.notebook_data[player_name][category_name].items():
                    if (item_name not in table[category_name].keys()):
                        table[category_name][item_name] = []

                    table[category_name][item_name].append(item)

        return table

if __name__ == '__main__':
    notebook = Notebook('Me')
    notebook.add_player('Grey')
    notebook.set_cell('Me', 'Weapons', 'Rope', 'X')

    data = notebook.notebook_data
    print("NOTEBOOK:", data)

    table = notebook.get_table()
    print("TABLE:", table)

    # calculate max spaces to line up label column
    max_item_name_length = 0
    for category_name, category in table.items():
        new_max = max(len(item_name) for item_name in category.keys())
        if new_max > max_item_name_length:
            max_item_name_length = new_max

    # calculate max spaces to line up player columns
    max_player_length = max(len(player_name) for player_name in data.keys())

    # Print the table header
    header = 'PLAYERS'
    print(f'{header:{max_item_name_length}} | ', end='')
    for player in data.keys():
        print(f'{player:{max_player_length}} | ', end='')
    print()

    for category_name, category in table.items():
        print('\n' + category_name + ':')

        for item_name, item in category.items():
            print(f'{item_name:{max_item_name_length}} | ', end='')

            for player_val in item:
                if not player_val:
                    player_val = ''
                print(f'{player_val:{max_player_length}} | ', end='')

            print()