class Notebook:
    def __init__(self, rows, cols):
        self.cells = [[None for _ in range(cols)] for _ in range(rows)]
        self.rows = [str(i) for i in range(1, rows + 1)]
        self.cols = [chr(i) for i in range(65, 65 + cols)]  # ASCII values for uppercase letters
        self.markings = {}

    def setCell(self, row, col, marking):
        """Sets the marking for a specific cell identified by row and column."""
        if row in self.rows and col in self.cols:
            self.cells[int(row) - 1][ord(col) - 65] = marking  # Convert to 0-based index
            self.markings[f'{row}{col}'] = marking
        else:
            print(f"Invalid row or column. Row should be in {self.rows} and column should be in {self.cols}.")


# Usage example:
# Create a 5x5 notebook
notebook = Notebook(5, 5)

# Set a cell marking
notebook.setCell('1', 'A', 'X')

# Check the current state of the cells
print(notebook.cells)

# Check the markings dictionary
print(notebook.markings)
