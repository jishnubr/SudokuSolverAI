import random

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_complete_board():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)
    return board
def remove_numbers_from_board(board, difficulty_level):
    attempts = difficulty_level
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        backup = board[row][col]
        board[row][col] = 0

        # Make a copy of the board to test if it still has a unique solution
        board_copy = [row[:] for row in board]
        if not solve_sudoku(board_copy):
            board[row][col] = backup
            attempts -= 1
        else:
            solve_sudoku(board_copy)
    return board
# Hybrid Solver
def hybrid_sudoku_solver(board):
    # Step 1: Initial Constraint Propagation
    constraint_propagation(board)
    
    # Step 2: Advanced Exact Cover with Dancing Links
    if dancing_links_algorithm(board):
        return True
    
    # Step 3: Stochastic Search Enhancements
    if stochastic_search(board):
        return True
    
    # Step 4: Backtracking with Optimizations
    return backtracking_with_optimizations(board)

# Generate a complex Sudoku puzzle
complete_board = generate_complete_board()
sudoku_puzzle = remove_numbers_from_board(complete_board, difficulty_level=5)  # Adjust difficulty_level as needed

print("Generated Sudoku Puzzle:")
print_board(sudoku_puzzle)

# Solve the generated Sudoku puzzle
if hybrid_sudoku_solver(sudoku_puzzle):
    print("Sudoku solved successfully!")
else:
    print("No solution exists.")

print_board(sudoku_puzzle)
