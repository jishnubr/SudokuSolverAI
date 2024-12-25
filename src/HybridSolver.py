import random
from Algorithms import backtracking_with_optimizations, constraint_propagation, dancing_links_algorithm, stochastic_search,hybrid_sudoku_solver

# Example Sudoku grid to test the solver
sudoku_grid = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0], 
    [5, 2, 0, 0, 0, 0, 0, 0, 0], 
    [0, 8, 7, 0, 0, 0, 0, 3, 1], 
    [0, 0, 3, 0, 1, 0, 0, 8, 0], 
    [9, 0, 0, 8, 6, 3, 0, 0, 5], 
    [0, 5, 0, 0, 9, 0, 6, 0, 0], 
    [1, 3, 0, 0, 0, 0, 2, 5, 0], 
    [0, 0, 0, 0, 0, 0, 0, 7, 4], 
    [0, 0, 5, 2, 0, 6, 3, 0, 0]
] 

if hybrid_sudoku_solver(sudoku_grid):
    print("Sudoku solved successfully!")
else:
    print("No solution exists.")

def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))

print_board(sudoku_grid)
