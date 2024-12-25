def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row = row // 3 * 3
    start_col = col // 3 * 3
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
                        print(f"Trying {num} at position ({row}, {col})")
                        
                        if solve_sudoku(board):
                            return True
                        
                        board[row][col] = 0
                        print(f"Backtracking from position ({row}, {col})")
                return False
    return True

def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))

# Example Sudoku grid to test the solver
test_sudoku_grid = [
    [0, 0, 0, 6, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 0, 3, 6, 0, 0],
    [0, 0, 0, 0, 9, 1, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 0, 3, 0, 6, 0, 4, 5],
    [0, 4, 0, 2, 0, 0, 0, 6, 0],
    [9, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 1, 0, 0]
]

if solve_sudoku(test_sudoku_grid):
    print("Sudoku solved successfully!")
else:
    print("No solution exists.")

print_board(test_sudoku_grid)

