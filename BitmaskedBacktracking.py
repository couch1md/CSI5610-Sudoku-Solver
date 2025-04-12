import copy, random

"""
Sodoku Solver using Backtracking with bit masking algorithm
This algortihm takes O(9^(n*n)) time complexity - with O(1) per step (number checking and placing)
and O(n) space complexity
"""
class SudokuSolver_BitmaskedBacktracking:
    """
    Initialize the Backtracking with bitmasking Sodoku Solver
    
    size: Dimension of board (e.g. 9 for 9x9 board)
    difficulty: (optional) Number of holes in the board
    matrix: (optional) 2D list of integers representing the initial board
    """
    def __init__(self, size, difficulty = None, matrix = None):
        # Bitmasking for rows, columns and small grids
        self.rows = [0] * size
        self.cols = [0] * size
        self.smallGrid = [0] * size

        # List of empty cell locations (row, col)
        self.empty = [] 
        self.dimension = size
        self.difficulty = difficulty
        self.smallGridDimension = int(size**0.5)

        # If no matrix is given, we will be generating a board
        if matrix == None:
            self.board = [[0 for _ in range(size)] for _ in range(size)]
            self.unsolved = [[0 for _ in range(size)] for _ in range(size)]
            self._initializeBitmask()
        # If a matrix is given, we will be solving the board
        else:
            self.board = copy.deepcopy(matrix)
            self.unsolved = copy.deepcopy(matrix)

####################
# Common Functions #
####################

    """
    Initialize the bitmask variables and collect empty cells
    """
    def _initializeBitmask(self):
        # Collect empty cells and initialize the bitmask variables
        for row in range(self.dimension):
            for col in range(self.dimension):
                # If cell is empty, add to list of empty cells
                if self.board[row][col] == 0:
                    self.empty.append((row, col))
                # Else, add the value to the bitmasks
                else:
                    self.rows[row] |= (1 << (self.board[row][col] - 1))
                    self.cols[col] |= (1 << (self.board[row][col] - 1))
                    location = (row // self.smallGridDimension) * self.smallGridDimension + (col // self.smallGridDimension)
                    self.smallGrid[location] |= (1 << (self.board[row][col] - 1))

    """
    Reset bitmask variables to 0
    """
    def _resetBitmasks(self):
        # Reset bitmasking for rows, columns and small grids to 0
        self.rows = [0] * self.dimension
        self.cols = [0] * self.dimension
        self.smallGrid = [0] * self.dimension
        
        # Reset the empty cell list to empty
        self.empty.clear()

    """
    Check if the number is valid at a given board position

    number: The number to check
    givenRow: The row of the given board position
    givenColumn: The column of the given board position
    """
    def _checkValid(self, number, givenRow, givenColumn):
        # Check if the number is already in the bitmasks
        checkRows = self.rows[givenRow] & (1 << (number - 1))
        checkCols = self.cols[givenColumn] & (1 << (number - 1))
        location = (givenRow // self.smallGridDimension) * self.smallGridDimension + (givenColumn // self.smallGridDimension) 
        checkSmallGrid = self.smallGrid[location] & (1 << (number - 1))
        # If the number is in any bitmask, it is not valid in the given location
        if checkRows or checkCols or checkSmallGrid:
            return False
        return True

    """
    Update the bitmask variables when placing or removing a number

    placing: True if placing a number, false if removing a number
    number: The number to place or remove
    givenRow: The row of the given board position
    givenColumn: The column of the given board position
    """
    def _updateBitmask(self, placing, number, givenRow, givenColumn):
        # If placing the number
        if placing:
            # Update the bitmask by setting the bit for the given number
            self.rows[givenRow] |= (1 << (number - 1))
            self.cols[givenColumn] |= (1 << (number - 1))
            location = (givenRow // self.smallGridDimension) * self.smallGridDimension + (givenColumn // self.smallGridDimension) 
            self.smallGrid[location] |= (1 << (number - 1))
        # If removing the number
        else:
            # Update the bitmask by clearing the bit for the given number
            self.rows[givenRow] &= ~(1 << (number - 1))
            self.cols[givenColumn] &= ~(1 << (number - 1))
            location = (givenRow // self.smallGridDimension) * self.smallGridDimension + (givenColumn // self.smallGridDimension) 
            self.smallGrid[location] &= ~(1 << (number - 1))

###########################
# Solving Board Functions #
###########################

    """
    Solve the Sodoku board using Backtracking algorithm

    gridLocation: The index of the empty cell in the empty list (row, col)
    """
    def solveBoard(self, gridLocation = 0):
        # If reach the end of the empty cells list, everything is filled
        if gridLocation == len(self.empty):
            return True
        
        # Get the next empty cell location (row, col) from empty list
        row, col = self.empty[gridLocation]

        # For each number from 1 to 9, check if it is valid at the current empty cell
        for number in range(1, self.dimension + 1):
            # Check if the number is valid in the current cell (check row, column, and small grid)
            if self._checkValid(number, row, col):
                # Place the number in the cell
                self.board[row][col] = number
                self._updateBitmask(True, number, row, col)

                # If recursive call returns True, the number is valid and board is solved
                if self.solveBoard(gridLocation + 1):
                    return True
                
                # If recursive call returns False, reset current cell back to 0 and try next number
                self.board[row][col] = 0
                self._updateBitmask(False, number, row, col)
        
        # If no valid solution can be found, return False
        return False
    
##############################
# Board Generation Functions #
##############################

    """
    Check if the number is valid in the small grid

    number: The number to verify
    row: The first row of the small grid
    column: The first column of the small grid
    """
    def _checkValidInSmallGrid(self, number, row, column):
        # Loop each row and column in the small grid
        for i in range(self.smallGridDimension):
            for j in range(self.smallGridDimension):
                # Return false if the number is already in the small grid
                if self.board[row + i][column + j] == number:
                    return False

        # Return true if the number is valid in the given small grid
        return True

    """
    Fill individual small grid on the diagonal with random numbers
    
    row: The first row of the small grid
    column: The first column of the small grid
    """
    def _fillSmallGrid(self, row, column):
        # Loop the number of rows and colums in the small grid
        for i in range(self.smallGridDimension):
            for j in range(self.smallGridDimension):
                # Loop until a valid number is generated
                while True:
                    number = random.randint(1, self.dimension)
                    if self._checkValidInSmallGrid(number, row, column):
                        break
                # Set the board position to the generated number if valid
                self.board[row + i][column + j] = number

    """
    Fill all diagonal small grids
    """
    def _fillAllDiagonalSmallGrids(self):
        # Fill the diagonal small grids
        for smallGrid in range(0, self.dimension, self.smallGridDimension):
            # Fill the small grid with the given starting row and column (top left corner of sub-grid)
            self._fillSmallGrid(smallGrid, smallGrid)

    """
    Remove numbers from the board to create the puzzle
    """
    def _removeNumbers(self):
        # Randomly remove a number until achieve the desired number of holes
        while self.difficulty > 0:
            # Generate random row and column
            row = random.randint(0, self.dimension - 1)
            column = random.randint(0, self.dimension - 1)

            # Check if the cell is not empty already
            if self.board[row][column] != 0:
                # Remove the number from the cell
                self.board[row][column] = 0

                # Decrease hole counter
                self.difficulty -= 1

    """
    Generate a valid Sodoku board
    """
    def generatePuzzle(self):
        # Fill diagonal small grids
        self._fillAllDiagonalSmallGrids()
        self._initializeBitmask()
        self.empty = [(row, col) for row in range(self.dimension) for col in range(self.dimension) if self.board[row][col] == 0]

        # Solve the rest of the board
        self.solveBoard()

        # Remove numbers based on difficulty level
        self._removeNumbers()

        # Initialize the bitmask for the generated board
        self._resetBitmasks()
        self._initializeBitmask()

        # Create a copy of the intial board for printing
        self.unsolved = copy.deepcopy(self.board)