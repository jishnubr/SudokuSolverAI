import random
from Algorithms import hybrid_sudoku_solver, is_valid

def generate_shuffled_board():
    base = 3
    side = base * base

    # Pattern for a baseline valid solution
    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    # Randomize rows, columns, and numbers (of valid base pattern)
    def shuffle(s): return random.sample(s, len(s))

    r_base = range(base)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, base * base + 1))

    # Produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    return board

def count_solutions(board):
    solutions = []
    def hybrid_sudoku_solver(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            hybrid_sudoku_solver(board)
                            board[row][col] = 0
                    return
        solutions.append([row[:] for row in board])

    hybrid_sudoku_solver(board)
    return len(solutions)

def remove_numbers_from_board(board, difficulty_level, max_attempts=100):
    attempts = 0
    removed_positions = []

    while attempts < difficulty_level and len(removed_positions) < 81:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        
        backup = board[row][col]
        board[row][col] = 0

        # More strategic removal can be applied here by prioritizing specific positions
        if count_solutions(board) != 1:
            board[row][col] = backup
        else:
            removed_positions.append((row, col))
        
        attempts += 1

    return board

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

# Generate a complete and shuffled Sudoku board
complete_board = generate_shuffled_board()

print("Generated Complete Board:")
print_board(complete_board)

# Create a Sudoku puzzle by removing numbers
difficulty_level = 64  # Adjust difficulty level as needed
sudoku_puzzle = remove_numbers_from_board(complete_board, difficulty_level, max_attempts=500)

print("Generated Sudoku Puzzle:")
print_board(sudoku_puzzle)

# Solve the generated Sudoku puzzle
if hybrid_sudoku_solver(sudoku_puzzle):
    print("Sudoku solved successfully!")
else:
    print("No solution exists.")

print("Solved Sudoku:")
print_board(sudoku_puzzle)

