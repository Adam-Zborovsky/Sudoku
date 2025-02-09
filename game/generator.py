import random
from constants.settings import DIFFICULTY_LEVELS

class SudokuGenerator:
    def generate_puzzle(self, difficulty):
        # First generate a complete solution
        solution = self._generate_solution()
        # Then create puzzle by removing numbers
        cells_to_remove = self._get_cells_to_remove(difficulty)
        puzzle = [[x for x in row] for row in solution]
        
        for row, col in cells_to_remove:
            puzzle[row][col] = 0
            
        return puzzle, solution
        
    def _generate_solution(self):
        # Initialize empty 9x9 grid
        grid = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_grid(grid)
        return grid
        
    def _fill_grid(self, grid, row=0, col=0):
        if col == 9:
            row += 1
            col = 0
        if row == 9:
            return True
            
        if grid[row][col] != 0:
            return self._fill_grid(grid, row, col + 1)
            
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self._is_valid(grid, row, col, num):
                grid[row][col] = num
                if self._fill_grid(grid, row, col + 1):
                    return True
                grid[row][col] = 0
        return False
        
    def _is_valid(self, grid, row, col, num):
        # Check row
        if num in grid[row]:
            return False
            
        # Check column
        if num in [grid[i][col] for i in range(9)]:
            return False
            
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num:
                    return False
        return True
        
    def _get_cells_to_remove(self, difficulty):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        # Number of cells to remove based on difficulty
        remove_count = {
            'Easy': 40,
            'Medium': 45,
            'Hard': 50,
            'Expert': 55
        }.get(difficulty, 40)
        
        return cells[:remove_count] 