from board import Board

class Notebook:
    def __init__(self):
        # Example structure for the notebook

        self.empty = {
            'Suspects': {},
            'Weapons': {},
            'Rooms': {}
        }

        for sus in Board.CHARACTERS:
            self.empty['Suspects'][sus] = None
        for wep in Board.WEAPONS:
            self.empty['Weapons'][wep] = None
        for room in Board.ROOMS:
            if ('Hallway' not in room):
                self.empty['Rooms'][room] = None

        self.notebook_data = {
            'Me' : self.empty,
        }

    def set_cell(self, player, category, item, marking):
        '''Sets the marking for a specific cell.'''
        if (player in self.notebook_data) and (category in self.notebook_data[player]) and (item in self.notebook_data[player][category]):
            self.notebook_data[player][category][item] = marking
        else:
            print(f'Invalid entry: {player}, {category}')

    def get_table(self):
        table = {}

        for player_name, player in self.notebook_data.items():
            for category_name, category in self.notebook_data[player_name].items():
                if (category_name not in table.keys()):
                    table[category_name] = {}

                for item_name, item in self.notebook_data[player_name][category_name].items():

                    if (item_name not in table.keys()):
                        table[category_name][item_name] = []

                    table[category_name][item_name].append(item)

        return table

if __name__ == '__main__':
    notebook = Notebook()
    notebook.set_cell('Me', 'Weapons', 'Rope', 'X')

    data = notebook.notebook_data

    # Print the table header
    print('PLAYERS: | ', end='')
    for player in data.keys():
        print(player + ' | ', end='')
    print()

    table = notebook.get_table()

    for category_name, category in table.items():
        print('\n' + category_name + ':')
        for item_name, item in table[category_name].items():
            print(item_name + ': | ', end='')

            for player_val in table[category_name][item_name]:
                if not player_val:
                    player_val = ''
                print(player_val + ' | ', end='')

            print()