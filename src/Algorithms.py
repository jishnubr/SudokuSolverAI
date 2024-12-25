import random

# Node and ColumnNode for DLX
class Node:
    def __init__(self, row=None, col=None):
        self.left = self.right = self.up = self.down = self
        self.column = col
        self.row = row

class ColumnNode(Node):
    def __init__(self, col=None):
        super().__init__(col=col)
        self.size = 0

# Dancing Links (DLX) structure
class DancingLinks:
    def __init__(self):
        self.header = ColumnNode()
        self.columns = []
    
    def add_column(self, col):
        new_col = ColumnNode(col)
        self.columns.append(new_col)
        self._append_to_right(self.header, new_col)
        return new_col
    
    def add_row(self, col_nodes):
        first_node = None
        for col in col_nodes:
            new_node = Node(row=len(self.columns), col=col)
            col.up.down = new_node
            new_node.up = col.up
            new_node.down = col
            col.up = new_node
            col.size += 1
            if first_node is None:
                first_node = new_node
            self._append_to_right(first_node, new_node)
    
    def _append_to_right(self, left_node, right_node):
        right_node.right = left_node.right
        right_node.right.left = right_node
        right_node.left = left_node
        left_node.right = right_node

# DLX Solver
class DLXSolver:
    def __init__(self, dlx):
        self.dlx = dlx
        self.solution = []
    
    def search(self, k=0):
        if self.dlx.header.right == self.dlx.header:
            return True
        col = self.select_column()
        self.cover_column(col)
        row = col.down
        while row != col:
            self.solution.append(row)
            right_node = row.right
            while right_node != row:
                self.cover_column(right_node.column)
                right_node = right_node.right
            if self.search(k + 1):
                return True
            row = self.solution.pop()
            col = row.column
            left_node = row.left
            while left_node != row:
                self.uncover_column(left_node.column)
                left_node = left_node.left
            row = row.down
        self.uncover_column(col)
        return False
    
    def select_column(self):
        col = self.dlx.header.right
        min_size = col.size
        best_col = col
        while col != self.dlx.header:
            if col.size < min_size:
                min_size = col.size
                best_col = col
            col = col.right
        return best_col
    
    def cover_column(self, col):
        col.right.left = col.left
        col.left.right = col.right
        row = col.down
        while row != col:
            right_node = row.right
            while right_node != row:
                right_node.down.up = right_node.up
                right_node.up.down = right_node.down
                right_node.column.size -= 1
                right_node = right_node.right
            row = row.down
    
    def uncover_column(self, col):
        row = col.up
        while row != col:
            left_node = row.left
            while left_node != row:
                left_node.column.size += 1
                left_node.down.up = left_node
                left_node.up.down = left_node
                left_node = left_node.left
            row = row.up
        col.right.left = col
        col.left.right = col
# Construct Exact Cover Matrix for Sudoku
def construct_exact_cover(board):
    # Define constraint types
    constraints = []
    for row in range(9):
        for col in range(9):
            constraints.append(('cell', row, col))
            for num in range(1, 10):
                constraints.append(('row', row, num))
                constraints.append(('col', col, num))
                constraints.append(('box', row // 3, col // 3, num))
    
    # Create an empty DLX structure
    dlx = DancingLinks()
    constraint_nodes = {}
    
    for constraint in constraints:
        constraint_nodes[constraint] = dlx.add_column(constraint)
    
    # Add rows to the DLX matrix based on the initial board
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                num = board[row][col]
                add_sudoku_row(dlx, constraint_nodes, row, col, num)
            else:
                for num in range(1, 10):
                    add_sudoku_row(dlx, constraint_nodes, row, col, num)
    
    return dlx

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
def add_sudoku_row(dlx, constraint_nodes, row, col, num):
    cell_constraint = ('cell', row, col)
    row_constraint = ('row', row, num)
    col_constraint = ('col', col, num)
    box_constraint = ('box', row // 3, col // 3, num)
    
    dlx.add_row([constraint_nodes[cell_constraint],
                 constraint_nodes[row_constraint],
                 constraint_nodes[col_constraint],
                 constraint_nodes[box_constraint]])

def dancing_links_algorithm(board):
    dlx = construct_exact_cover(board)
    solver = DLXSolver(dlx)
    
    return solver.search()

# Constraint Propagation
def possible_values(board, row, col):
    if board[row][col] != 0:
        return []
    
    values = set(range(1, 10))
    
    values -= {board[row][i] for i in range(9)}
    values -= {board[i][col] for i in range(9)}
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    values -= {board[i][j] for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)}
    
    return list(values)

def constraint_propagation(board):
    changed = True
    while changed:
        changed = False
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    values = possible_values(board, row, col)
                    if len(values) == 1:
                        board[row][col] = values[0]
                        changed = True

# Stochastic Search
def stochastic_search(board):
    def random_solver(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    values = possible_values(board, row, col)
                    if not values:
                        return False
                    num = random.choice(values)
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if random_solver(board):
                            return True
                        board[row][col] = 0
                    return False
        return True
    
    return random_solver(board)

# Backtracking with Optimizations
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

def backtracking_with_optimizations(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if backtracking_with_optimizations(board):
                            return True
                        board[row][col] = 0
                return False
    return True

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