
# CSI-5610 - Sudoku Solver

This is the final project for Matthew Couch for CSI-5610. This project was created to investigate different algorithms that can be used for solving Sudoku puzzles. 


## Background

Below is a short explanation of each of the three algorithms used: Backtracking, Bitmasked Backtracking, and Simulated Annealing

### Backtracking

Backtracking is a naive approach to solving the Sudoku problem. It attempts to fill each unassigned cell with a valid number, then checks the cells row, column, and small grid for the number it just assigned. If it is already present, it will backtrack to find a number that works. This is a brute force way of solving the Sudoku algorithm. It can be done in O(n*9^(n*n)) time complexity, were n = dimension (e.g. 9 for 9x9 boards) and O(1) space complexity. 

### Bitmasked Backtracking

Bitmasked Backtracking is similar to Backtracking, except slightly optimized using bit masking. To incorporate this idea, extra arrays are created for rows, columns, and small grids of size n. These are used to denote the used values within each respective group. Setting the bit in these arrays means that the value is used, and unsetting the bit means it is not used. This speeds up the time complexity of the algorithm to be O(9^(n*n)) and keeps the O(1) space complexity. 

### Simulated Annealing

Simulated Annealing is a form of Stochastic Search Algorithms that is inspired by the annealing process in metallurgy. In this process, metals are heated and cooled gradually to remove defects. The same is true in coding, you start at a high temperature and cool it through iterations of solutions. It helps escapte local optima through the use of probabilistic acceptance. Unlike backtracking, we start with an initial solution and then swap neighbor cells to calculate a new cost (number of duplicate numbers in rows, columns and small grids). Then the probablility of acceptance is calculated and the new board is either accepted or rejected. Lastly, the temperature is cooled (changing the probablility of acceptance). This solution can be done in O(k) time complexity, where k = number of iterations, and O(1) space complexity. 
## Deployment / Usage

1. Run the main script "SudokuSolver.py"
2. Enter the algorithm you want to use: (1) Backtracking, (2) Bitmasked Backtracking, (3) Stochastic Search (Simulated Annealing)
3. Enter the size of the Sudoku Board you want to use (e.g. 4 for 4x4, 9 for 9x9, 16 for 16x16)
4. Enter if you want to (1) Generate a board or (2) Provide a board

        If (1) Generate a board
            1. Enter difficulty (Easy, Medium, Hard, Extreme)
        If (2) Provide a board
            1. Provide each row individually with each number separated by spaces and holes represented by 0's
                (e.g: Row 1: 0 0 0 0 0 0 0 0 0)
5. Enter to repeat, or type "exit" to quit application


Example: 
```bash
  $ python3 ./SudokuSolver.py 
  Enter the algorithm to use: (1) Backtracking, (2) Bitmasked Backtracking, (3) Stochastic Search (Simulated Annealing): 1

  Enter the size of the Sudoku board (e.g. 4 for 4x4, 9 for 9x9, 16 for 16x16): 9

  Do you want to (1) Generate a board or (2) Provide a borad? 1

  Enter difficulty (Easy, Medium, Hard, Extreme): hard

  Initial Board:
   -----------------------
  | 0 7 9 | 3 0 5 | 0 6 0 |
  | 6 2 8 | 0 4 0 | 3 0 5 |
  | 4 3 5 | 0 8 0 | 0 7 0 |
   -----------------------
  | 0 0 0 | 0 0 0 | 9 0 3 |
  | 2 1 0 | 5 0 0 | 7 0 6 |
  | 0 0 0 | 7 3 4 | 0 1 2 |
   -----------------------
  | 7 8 0 | 0 1 0 | 6 5 4 |
  | 0 6 4 | 0 0 2 | 1 0 0 |
  | 0 0 0 | 0 7 6 | 0 2 0 |
   -----------------------
  Solving Sodoku using Backtracking...
   -----------------------
  | 1 7 9 | 3 2 5 | 4 6 8 |
  | 6 2 8 | 1 4 7 | 3 9 5 |
  | 4 3 5 | 6 8 9 | 2 7 1 |
   -----------------------
  | 5 4 7 | 2 6 1 | 9 8 3 |
  | 2 1 3 | 5 9 8 | 7 4 6 |
  | 8 9 6 | 7 3 4 | 5 1 2 |
   -----------------------
  | 7 8 2 | 9 1 3 | 6 5 4 |
  | 9 6 4 | 8 5 2 | 1 3 7 |
  | 3 5 1 | 4 7 6 | 8 2 9 |
   -----------------------
  Press Enter to generate a new board or 'exit' to quit:
  Enter the algorithm to use: (1) Backtracking, (2) Bitmasked Backtracking, (3) Stochastic Search (Simulated Annealing): 1

  Enter the size of the Sudoku board (e.g. 4 for 4x4, 9 for 9x9, 16 for 16x16): 9

  Do you want to (1) Generate a board or (2) Provide a borad? 2
  Please enter 9 numbers between 0 and 9 separated by spaces (use 0 for empty cells):
  Row 1: 3 0 6 5 0 8 4 0 0
  Row 2: 5 2 0 0 0 0 0 0 0
  Row 3: 0 8 7 0 0 0 0 3 1
  Row 4: 0 0 3 0 1 0 0 8 0
  Row 5: 9 0 0 8 6 3 0 0 5
  Row 6: 0 5 0 0 9 0 6 0 0
  Row 7: 1 3 0 0 0 0 2 5 0
  Row 8: 0 0 0 0 0 0 0 7 4
  Row 9: 0 0 5 2 0 6 3 0 0

  Initial Board:
   -----------------------
  | 3 0 6 | 5 0 8 | 4 0 0 |
  | 5 2 0 | 0 0 0 | 0 0 0 |
  | 0 8 7 | 0 0 0 | 0 3 1 |
   -----------------------
  | 0 0 3 | 0 1 0 | 0 8 0 |
  | 9 0 0 | 8 6 3 | 0 0 5 |
  | 0 5 0 | 0 9 0 | 6 0 0 |
   -----------------------
  | 1 3 0 | 0 0 0 | 2 5 0 |
  | 0 0 0 | 0 0 0 | 0 7 4 |
  | 0 0 5 | 2 0 6 | 3 0 0 |
   -----------------------
  Solving Sodoku using Backtracking...
   -----------------------
  | 3 1 6 | 5 7 8 | 4 9 2 |
  | 5 2 9 | 1 3 4 | 7 6 8 |
  | 4 8 7 | 6 2 9 | 5 3 1 |
   -----------------------
  | 2 6 3 | 4 1 5 | 9 8 7 |
  | 9 7 4 | 8 6 3 | 1 2 5 |
  | 8 5 1 | 7 9 2 | 6 4 3 |
   -----------------------
  | 1 3 8 | 9 4 7 | 2 5 6 |
  | 6 9 2 | 3 5 1 | 8 7 4 |
  | 7 4 5 | 2 8 6 | 3 1 9 |
   -----------------------
  Press Enter to generate a new board or 'exit' to quit: exit
  Thanks for playing!
```


## References

 - [Backtracking and Bitmasked Backtracking](https://www.geeksforgeeks.org/sudoku-backtracking-7/)
 - [Stochastic Search - Simulated Annealing](https://www.geeksforgeeks.org/local-search-algorithm-in-artificial-intelligence/#2-simulated-annealing)

