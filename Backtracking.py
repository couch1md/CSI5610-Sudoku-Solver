import copy, random

"""
Sodoku Solver using Backtracking algorithm (Brute force)
This algortihm takes O(9^n) time complexity and O(1) space complexity
"""
class SudokuSolver_Backtracking:
    """
    Initialize the Backtracking Sodoku Solver
    
    size: Dimension of board (e.g. 9 for 9x9 board)
    difficulty: (optional) Number of holes in the board
    matrix: (optional) 2D list of integers representing the initial board
    """
    def __init__(self, size, difficulty = None, matrix = None):
        # If no matrix is given, we will be generating a board
        if matrix == None:
            self.board = [[0 for _ in range(size)] for _ in range(size)]
            self.unsolved = [[0 for _ in range(size)] for _ in range(size)]
        # If a matrix is given, we will be solving the board
        else:
            self.board = copy.deepcopy(matrix)
            self.unsolved = copy.deepcopy(matrix)
        self.dimension = size
        self.difficulty = difficulty
        self.smallGridDimension = int(size**0.5)

####################
# Common Functions #
####################

    """
    Check if the number is valid at a given board position

    number: The number to check
    givenRow: The row of the given board position
    givenColumn: The column of the given board position
    """
    def _checkValid(self, number, givenRow, givenColumn):
        # Check row and column for the number
        for num in range(self.dimension):
            # Check if the number is already in the given row
            if self.board[givenRow][num] == number:
                return False
            # Check if the number is already in the given column
            if self.board[num][givenColumn] == number:
                return False

        # Check if the number is already in the given row/column small grid
        smallGridStartRow = givenRow - givenRow % self.smallGridDimension
        smallGridStartColumn = givenColumn - givenColumn % self.smallGridDimension
        # Loop each row and column in the small grid
        for i in range(self.smallGridDimension):
            for j in range(self.smallGridDimension):
                if self.board[smallGridStartRow + i][smallGridStartColumn + j] == number:
                    return False

        # Return true if the number is valid in the given grid location
        return True

###########################
# Solving Board Functions #
###########################

    """
    Solve the Sodoku board using Backtracking algorithm

    row: The current row to check (starting at 0)
    column: The current column to check (starting at 0)
    """
    def solveBoard(self, row = 0, column = 0):
        # If at the final cell of the board (board already solved), return True
        if row == self.dimension - 1 and column == self.dimension:
            return True
        
        # If end of row, move to next row and reset column to 0
        if column == self.dimension:
            row += 1
            column = 0

        # If the current cell is filled, move to next cell
        if self.board[row][column] != 0:
            return self.solveBoard(row, column + 1)
        
        # Try each number in the current cell
        for number in range(1, self.dimension + 1):
            # Check if the number is valid in the current cell (check row, column, and small grid)
            if self._checkValid(number, row, column):
                # If valid, place the number in the cell
                self.board[row][column] = number
                
                # If recursive call returns True, the number is valid and board is solved
                if self.solveBoard(row, column +1):
                    return True
                
                # If recursive call returns False, reset current cell back to 0 and try next number
                self.board[row][column] = 0

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

        # Fill the rest of the board
        self.solveBoard()
        #self.fillRemainingCells()

        # Remove numbers based on difficulty level
        self._removeNumbers()

        # Create a copy of the intial board for printing
        self.unsolved = copy.deepcopy(self.board)