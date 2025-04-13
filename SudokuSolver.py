from Backtracking import SudokuSolver_Backtracking
from BitmaskedBacktracking import SudokuSolver_BitmaskedBacktracking
from StochasticSearch import SudokuSolver_StochasticSearch
import math

"""
CONSTANT for printing board based on small grid size
"""
BOARD_LENGTH = {
    2 : 11, 
    3 : 23, 
    4 : 55
}

"""
CONSTANT for the algorithms that can be used to solve the Sudoku puzzle
"""
ALGORITHMS = {
    "1": "Backtracking",
    "2": "Bitmasked Backtracking",
    "3": "Stochastic Search (Simulated Annealing)"
}

"""
Print the Sodoku Board (Not used in the GUI implementation)

board: The solved board
unsolvedBoard: The original puzzle board with "empty" cells 
smallGridDimension: The size of the small sub-grid
"""
def printSodokuBoard(board, unsolvedBoard, smallGridDimension):
    # Length of board based on small grid size
    length = BOARD_LENGTH[smallGridDimension]
    # Print a horizontal line at the top of the board
    print(" " + "-" * length)
    # Loop each row in the board
    for i, row in enumerate(board):
        # Print a horizontal line after every sub-grid
        if i % smallGridDimension == 0 and i != 0:
            print(" " + "-" * length)
        # Loop each column position in each row
        for j, cell in enumerate(row):
            # Print a vertical line every 3 positions (including at the beginning)
            if j % smallGridDimension == 0:
                print("| ", end="")
            # Print the number at the grid position (White for given puzzle, Cyan for generated solution)
            if unsolvedBoard[i][j] > 0:
                # Make each digit 2 spaces if board larger than 9x9
                if smallGridDimension > 3: 
                    print(f"\033[97m{cell if len(str(cell)) != 1 else " " + str(cell)}\033[0m", end=" ")
                # Make each digit 1 space if board smaller or equal to 9x9
                else:
                    print(f"\033[97m{cell}\033[0m", end=" ")
            else:
                # Make each digit 2 spaces if board larger than 9x9
                if smallGridDimension > 3: 
                    print(f"\033[36m{cell if len(str(cell)) != 1 else " " + str(cell)}\033[0m", end=" ")
                # Make each digit 1 space if board smaller or equal to 9x9
                else:
                    print(f"\033[36m{cell}\033[0m", end=" ")
        # Print a vertical line at the end of each row
        print("|")
    # Print a horizontal line at the bottom of the board
    print(" " + "-" * length)

"""
Grab board from user input if the user wants to provide one

size: The dimension of the board
"""
def getUserInputtedBoard(size):
    # Initialize an empty board to fill with user input
    board = [[0 for _ in range(size)] for _ in range(size)]
    
    # Ask for user input
    print(f"Please enter {size} numbers between 0 and {size} separated by spaces (use 0 for empty cells):")
    for row in range(size):
        # Loop for the number of rows in the board
        while True:
            # Try to add the row to the list if provided correctly
            try:
                # Get the row from the user
                givenRow = list(map(int, input(f"Row {row + 1}: ").strip().split()))
                # If the row is not the right size or contains invalid numbers, raise an error
                if len(givenRow) != size or all(number < 0 or number > size for number in givenRow):
                    raise ValueError
                # Add the new row to the board, and then ask for next row
                board[row] = givenRow
                break
            # If the row is not the right size or contains invalid numbers, raise an error
            except ValueError:
                print(f"Invalid input. Please enter {size} numbers between 0 and {size} separated by spaces.")
    
    # Return the user inputted puzzle board
    return board

"""
Determine the difficulty of the Sodoku board by deciding the number of empty cells

size: The size of the board
"""
def determineDifficulty(size):
    # Manually set difficulty levels for 4x4 grids
    if size == 4:
        difficulties = {"easy": 2, "medium": 3, "hard": 4, "extreme": 5}
    # Else, set difficulty based on size of the board
    else:
        difficulties = {"easy": size ** 2 // 3, "medium": size ** 2 // 2.5, "hard": size ** 2 // 2, "extreme": size ** 2 // 1.5}

    # Ask user for difficulty level
    while True:
        difficulty = input("\nEnter difficulty (Easy, Medium, Hard, Extreme): ").strip().lower()
        if difficulty in difficulties:
            return difficulties[difficulty]
        print("Invalid difficulty... Please enter Easy, Medium, Hard, or Extreme.")

"""
Function to manage the game loop and user input
"""
def sudoku():
    # Ask user for search algorithm to use
    while True:
        algorithm = input("Enter the algorithm to use: (1) Backtracking, (2) Bitmasked Backtracking, (3) Stochastic Search (Simulated Annealing): ")
        if algorithm in ["1", "2", "3"]:
            break
        print("Invalid input. Please enter 1, 2, or 3.")

    # Ask user for the size of the board and difficulty level
    while True:
        size = int(input("\nEnter the size of the Sudoku board (e.g. 4 for 4x4, 9 for 9x9, 16 for 16x16): "))
        if math.sqrt(size) == int(size**0.5):
            break
        print("Invalid size. Please enter a perfect square (e.g. 4, 9, 16, etc.).")
    
    # Ask if the user wants to provide a board or generate one
    generate = input("\nDo you want to (1) Generate a board or (2) Provide a borad? ")
    
    # If user wants to generate a board, ask for difficulty level
    if generate == "1":
        # Determine the difficulty level of the board
        difficulty = determineDifficulty(size)
    # If user wants to provide a board, ask for the board
    elif generate == "2":
        # Ask for the board from the user
        board = getUserInputtedBoard(size)

    # If (1) is selected, initialize the Backtracking Sodoku Solver
    if algorithm == "1":
        # If the user wants to generate a board, initiailze and generate a board using Backtracking algorithm
        if generate == "1":
            # Initialize the Backtracking Sodoku Solver
            board = SudokuSolver_Backtracking(size, difficulty)

            # Generate a puzzle using the Backtracking algorithm
            board.generatePuzzle()

        # If the user wants to provide a board, initialize the Backtracking Sodoku Solver with the provided board
        elif generate == "2":
            # Initialize the Backtracking Sodoku Solver with the provided board
            board = SudokuSolver_Backtracking(size, matrix=board)
   
    # If (2) is selected, initialize the Bitmasked Backtracking Sodoku Solver
    elif algorithm == "2":
        # If the user wants to generate a board, initiailze and generate a board using Backtracking algorithm
        if generate == "1":
            # Initialize the Backtracking Sodoku Solver
            board = SudokuSolver_BitmaskedBacktracking(size, difficulty)

            # Generate a puzzle using the Backtracking algorithm
            board.generatePuzzle()

        # If the user wants to provide a board, initialize the Backtracking Sodoku Solver with the provided board
        elif generate == "2":
            # Initialize the Backtracking Sodoku Solver with the provided board
            board = SudokuSolver_BitmaskedBacktracking(size, matrix=board)
    
    # If (3) is selected, initialize the Stochastic Search Sodoku Solver
    elif algorithm == "3":
        # If the user wants to generate a board, initiailze and generate a board using Backtracking algorithm
        if generate == "1":
            # Initialize a board using backtracking algorithm
            generatedBoard = SudokuSolver_Backtracking(size, difficulty)
            generatedBoard.generatePuzzle()

            # Initialize the Stochastic Search Sodoku Solver
            board = SudokuSolver_StochasticSearch(size, matrix=generatedBoard.board)

        # If the user wants to provide a board, initialize the Backtracking Sodoku Solver with the provided board
        elif generate == "2":
            # Initialize the Backtracking Sodoku Solver with the provided board
            board = SudokuSolver_StochasticSearch(size, matrix=board)

    # Print the initial board with 0s as empty locations
    print("\nInitial Board: ")
    printSodokuBoard(board.board, board.unsolved, board.smallGridDimension)

    # Solve the Sodoku board using the selected algorithm
    print(f"Solving Sodoku using {ALGORITHMS[algorithm]}...")
    if board.solveBoard():
       printSodokuBoard(board.board, board.unsolved, board.smallGridDimension)
    else: 
       print("Sodoku cannot be solved.")

"""
Main function to run the Sudoku Solver (Loop until user quits)
"""
if __name__ == "__main__":
    while True:
        sudoku()
        user_input = input("Press Enter to generate a new board or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Thanks for playing!")
            break