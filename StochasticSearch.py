import copy, random, math

"""
Sodoku Solver using Stochastic Search algorithm (Simulated Annealing)
This algortihm takes O(k) time complexity (k = number of iterations) and O(1) space complexity
"""
class SudokuSolver_StochasticSearch:
    """
    Initialize the Stochastic Search Sodoku Solver using Simulated Annealing
    
    size: Dimension of board (e.g. 9 for 9x9 board)
    difficulty: (optional) Number of holes in the board
    matrix: (optional) 2D list of integers representing the initial board
    """
    def __init__(self, size, difficulty = None, matrix = None):    
        self.dimension = size
        #self.difficulty = difficulty
        self.smallGridDimension = int(size**0.5)

        self.maxIterations = 100000
        self.temperature = 5.0
        self.coolingRate = 0.999

        # # If no matrix is given, we will be generating a board
        # if matrix == None:
        #     self.board = [[0 for _ in range(size)] for _ in range(size)]
        #     self.unsolved = [[0 for _ in range(size)] for _ in range(size)]
        # # If a matrix is given, we will be solving the board
        # else:
        self.board = copy.deepcopy(matrix)
        self.unsolved = copy.deepcopy(matrix)
        self.unsolvedBoard = [[num != 0 for num in row] for row in matrix]
        self.nonFixedCells = [
            (row, col) for row in range(size) for col in range(size) if matrix[row][col] == 0
        ]
        self._initializeBoard()

    """
    Initialize the board with random numbers, ensuring unique numbers in each small grid
    """
    def _initializeBoard(self):
        # Initialize the board with random numbers
        for row in range(0, self.dimension, self.smallGridDimension):
            for col in range(0, self.dimension, self.smallGridDimension):
                self._fillSmallGrid(row // self.smallGridDimension, col // self.smallGridDimension)

    """
    Fill individual small grids

    row: The first row of the small grid
    column: The first column of the small grid
    """
    def _fillSmallGrid(self, row, column):
        # Loop the number of rows and colums in the small grid
        for i in range(row * self.smallGridDimension, row * self.smallGridDimension + self.smallGridDimension):
            for j in range(column * self.smallGridDimension, column * self.smallGridDimension + self.smallGridDimension):
                # If the cell is empty, generate a random number
                if not self.unsolvedBoard[i][j]:
                    # Loop until a valid number is generated
                    while True:
                        number = random.randint(1, self.dimension)
                        if self._checkValidInSmallGrid(number, row, column):
                            break
                    # Set the board position to the generated number if valid
                    self.board[i][j] = number

    """
    Check if the number is valid in the small grid

    number: The number to verify
    row: The first row of the small grid
    column: The first column of the small grid
    """
    def _checkValidInSmallGrid(self, number, row, column):
        smallGridStartRow = row * self.smallGridDimension
        smallGridStartColumn = column * self.smallGridDimension
        # Loop each row and column in the small grid
        for i in range(self.smallGridDimension):
            for j in range(self.smallGridDimension):
                # Return false if the number is already in the small grid
                if self.board[smallGridStartRow + i][smallGridStartColumn + j] == number:
                    return False

        # Return true if the number is valid in the given small grid
        return True
    
    """
    Calculate the cost of the current board by counting the number of conflicts in the rows and columns
    """
    def _cost(self):
        # Initialize cost to 0
        cost = 0
        # Check rows and columns for conflicts
        for i in range(self.dimension):
            # Count the conflicts in each row
            cost += (self.dimension - len(set(self.board[i][j] for j in range(self.dimension))))
            # Count the conflicts in each column
            cost += (self.dimension - len(set(self.board[j][i] for j in range(self.dimension))))
        # Return total number of conflicts
        return cost
    
    """
    Find two random cells in the same small grid and swap their values if they are not a part of the original puzzle
    """
    def _getSwappedNeighbors(self):
        # Initialize the new board
        swappedNeighborBoard = copy.deepcopy(self.board)

        # Randomly select a small grid
        smallGridRow = random.randint(0, self.smallGridDimension - 1)
        smallGridColumn = random.randint(0, self.smallGridDimension - 1)

        # Find all non-fixed cells in the small grid
        nonFixedCells = [
            # Grab the position of the non-fixed cell
            (row, col)
            # Loop through the small grid
            for row in range(smallGridRow * self.smallGridDimension, smallGridRow * self.smallGridDimension + self.smallGridDimension)
            for col in range(smallGridColumn * self.smallGridDimension, smallGridColumn * self.smallGridDimension + self.smallGridDimension)
            # Add if not a part of the original puzzle
            if not self.unsolvedBoard[row][col]
        ]

        # If there are less than 2 non-fixed cells, cannot swap anything, return the original board
        if len(nonFixedCells) < 2:
            return swappedNeighborBoard
        
        # Randomly select two of the non-fixed numbers and swap them
        location1, location2 = random.sample(nonFixedCells, 2)
        number1 = swappedNeighborBoard[location1[0]][location1[1]]
        number2 = swappedNeighborBoard[location2[0]][location2[1]]
        swappedNeighborBoard[location1[0]][location1[1]] = number2
        swappedNeighborBoard[location2[0]][location2[1]] = number1

        # Return the new board with the swapped neighbors
        return swappedNeighborBoard
    
    """
    Solve the Sodoku board using Stochastic Search algorithm (Simulated Annealing)
    """
    def solveBoard(self):
        # Initialize variable for current board, cost, and temperature
        currentBoard = self.board
        currentCost = self._cost()
        temp = self.temperature

        # Loop for the number of iterations or until solution is found
        for _ in range(self.maxIterations):
            # If the current board cost is 0, the board is solved, return True
            if currentCost == 0:
                self.board = currentBoard
                return True
            
            # Get a new board by swapping two random numbers in the same small grid
            newBoard = self._getSwappedNeighbors()
            # Set the current board to the previous board
            previousBoard = self.board
            # Update the current board to the new board
            self.board = newBoard
            # Calculate the cost of the new board
            newCost = self._cost()

            # Calculate the cost difference between the new and previous boards
            deltaCost = newCost - currentCost
            
            # If the new board is better than the current board with by acceptance probability, take new board
            if deltaCost < 0 or random.random() < math.exp(-deltaCost / temp):
                # Accept the new board as the current board
                currentBoard = newBoard
                currentCost = newCost
            else:
                # Revert the current board back to the previous board
                self.board = previousBoard

            # Update the temperature
            temp = temp * self.coolingRate

        # If no valid solution can be found, return False
        return False