"""
Sudoku Solver - Command Line Version
A comprehensive CLI-based Sudoku solver with backtracking algorithm.
"""

import json
import time
import copy
import os
from datetime import datetime

class SudokuSolver:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_steps = []
        self.solve_time = 0
        
    def is_valid(self, grid, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        for x in range(9):
            if grid[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if grid[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def find_empty_cell(self, grid):
        """Find the next empty cell in the grid"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None
    
    def solve_sudoku(self, grid=None, record_steps=False):
        """Solve Sudoku using backtracking algorithm"""
        if grid is None:
            grid = self.grid
        
        if record_steps:
            self.solution_steps = []
        
        start_time = time.time()
        result = self._solve_recursive(grid, record_steps)
        self.solve_time = time.time() - start_time
        
        return result
    
    def _solve_recursive(self, grid, record_steps):
        """Recursive backtracking solver"""
        empty_cell = self.find_empty_cell(grid)
        if not empty_cell:
            return True  # Solved
        
        row, col = empty_cell
        
        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                
                if record_steps:
                    self.solution_steps.append((row, col, num, 'place'))
                
                if self._solve_recursive(grid, record_steps):
                    return True
                
                # Backtrack
                grid[row][col] = 0
                if record_steps:
                    self.solution_steps.append((row, col, 0, 'backtrack'))
        
        return False
    
    def is_valid_puzzle(self, grid):
        """Check if the puzzle is valid (no conflicts)"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    num = grid[i][j]
                    grid[i][j] = 0  # Temporarily remove to check
                    if not self.is_valid(grid, i, j, num):
                        grid[i][j] = num  # Restore
                        return False
                    grid[i][j] = num  # Restore
        return True
    
    def has_unique_solution(self, grid):
        """Check if the puzzle has a unique solution"""
        solutions = []
        test_grid = copy.deepcopy(grid)
        self._find_all_solutions(test_grid, solutions, max_solutions=2)
        return len(solutions) == 1
    
    def _find_all_solutions(self, grid, solutions, max_solutions=2):
        """Find all solutions (limited to max_solutions for efficiency)"""
        if len(solutions) >= max_solutions:
            return
        
        empty_cell = self.find_empty_cell(grid)
        if not empty_cell:
            solutions.append(copy.deepcopy(grid))
            return
        
        row, col = empty_cell
        
        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                self._find_all_solutions(grid, solutions, max_solutions)
                grid[row][col] = 0
    
    def get_difficulty_level(self, grid):
        """Estimate difficulty level based on number of given clues"""
        filled_cells = sum(row.count(0) for row in grid)
        empty_cells = 81 - filled_cells + sum(row.count(0) for row in grid)
        
        if empty_cells <= 40:
            return "Easy"
        elif empty_cells <= 50:
            return "Medium"
        elif empty_cells <= 60:
            return "Hard"
        else:
            return "Expert"
    
    def count_filled_cells(self, grid):
        """Count filled cells in the grid"""
        return sum(sum(1 for cell in row if cell != 0) for row in grid)
    
    def get_statistics(self, grid):
        """Get puzzle statistics"""
        filled = self.count_filled_cells(grid)
        empty = 81 - filled
        difficulty = self.get_difficulty_level(grid)
        
        return {
            'filled': filled,
            'empty': empty,
            'difficulty': difficulty,
            'completion': round((filled / 81) * 100, 1)
        }

class SudokuCLI:
    def __init__(self):
        self.solver = SudokuSolver()
        self.data_file = "sudoku_puzzles.json"
        self.load_puzzles()
    
    def print_grid(self, grid, highlight_original=False):
        """Print the Sudoku grid in a formatted way"""
        print("\n" + "═" * 37)
        print("         1 2 3   4 5 6   7 8 9")
        print("       ┌─────────┬─────────┬─────────┐")
        
        for i in range(9):
            if i > 0 and i % 3 == 0:
                print("       ├─────────┼─────────┼─────────┤")
            
            row_str = f"    {i+1}  │"
            for j in range(9):
                if j > 0 and j % 3 == 0:
                    row_str += "│"
                
                if grid[i][j] == 0:
                    row_str += " ."
                else:
                    if highlight_original and self.solver.original_grid[i][j] != 0:
                        row_str += f" {grid[i][j]}"  # Original numbers
                    else:
                        row_str += f" {grid[i][j]}"  # Solved numbers
                
                if j < 8:
                    row_str += " "
            
            row_str += " │"
            print(row_str)
        
        print("       └─────────┴─────────┴─────────┘")
    
    def print_colored_grid(self, grid):
        """Print grid with colors (if terminal supports it)"""
        print("\n" + "═" * 37)
        print("         1 2 3   4 5 6   7 8 9")
        print("       ┌─────────┬─────────┬─────────┐")
        
        for i in range(9):
            if i > 0 and i % 3 == 0:
                print("       ├─────────┼─────────┼─────────┤")
            
            row_str = f"    {i+1}  │"
            for j in range(9):
                if j > 0 and j % 3 == 0:
                    row_str += "│"
                
                if grid[i][j] == 0:
                    row_str += " ."
                else:
                    if self.solver.original_grid[i][j] != 0:
                        # Original numbers in blue
                        row_str += f" \033[94m{grid[i][j]}\033[0m"
                    else:
                        # Solved numbers in red
                        row_str += f" \033[91m{grid[i][j]}\033[0m"
                
                if j < 8:
                    row_str += " "
            
            row_str += " │"
            print(row_str)
        
        print("       └─────────┴─────────┴─────────┘")
    
    def input_puzzle(self):
        """Allow user to input a puzzle manually"""
        print("\n📝 Enter your Sudoku puzzle")
        print("=" * 50)
        print("Instructions:")
        print("• Enter numbers 1-9 for filled cells")
        print("• Use 0 or . for empty cells")
        print("• You can enter row by row or cell by cell")
        print("• Type 'cancel' to return to main menu")
        print()
        
        while True:
            method = input("Choose input method:\n1. Row by row\n2. Cell by cell\n3. Cancel\nEnter choice (1-3): ").strip()
            
            if method == '3' or method.lower() == 'cancel':
                return False
            elif method == '1':
                return self.input_by_rows()
            elif method == '2':
                return self.input_by_cells()
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    def input_by_rows(self):
        """Input puzzle row by row"""
        print("\n📝 Enter puzzle row by row (9 numbers each):")
        print("Example: 5 3 0 0 7 0 0 0 0")
        print()
        
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            while True:
                try:
                    row_input = input(f"Row {i+1}: ").strip()
                    if row_input.lower() == 'cancel':
                        return False
                    
                    # Parse input
                    numbers = []
                    for char in row_input.replace(' ', '').replace('.', '0'):
                        if char.isdigit():
                            numbers.append(int(char))
                    
                    if len(numbers) != 9:
                        print("❌ Please enter exactly 9 numbers.")
                        continue
                    
                    if any(num < 0 or num > 9 for num in numbers):
                        print("❌ Numbers must be between 0-9.")
                        continue
                    
                    grid[i] = numbers
                    break
                    
                except ValueError:
                    print("❌ Invalid input. Please enter numbers only.")
        
        self.solver.grid = grid
        self.solver.original_grid = copy.deepcopy(grid)
        return True
    
    def input_by_cells(self):
        """Input puzzle cell by cell"""
        print("\n📝 Enter puzzle cell by cell:")
        print("Format: row col value (e.g., 1 1 5)")
        print("Enter 'done' when finished, 'show' to see current grid")
        print()
        
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        while True:
            try:
                cell_input = input("Enter cell (row col value) or 'done'/'show': ").strip()
                
                if cell_input.lower() == 'done':
                    break
                elif cell_input.lower() == 'show':
                    self.print_grid(grid)
                    continue
                elif cell_input.lower() == 'cancel':
                    return False
                
                parts = cell_input.split()
                if len(parts) != 3:
                    print("❌ Format: row col value (e.g., 1 1 5)")
                    continue
                
                row, col, value = map(int, parts)
                
                if not (1 <= row <= 9 and 1 <= col <= 9):
                    print("❌ Row and column must be between 1-9")
                    continue
                
                if not (0 <= value <= 9):
                    print("❌ Value must be between 0-9")
                    continue
                
                grid[row-1][col-1] = value
                print(f"✅ Set cell ({row},{col}) to {value}")
                
            except ValueError:
                print("❌ Invalid input. Use numbers only.")
        
        self.solver.grid = grid
        self.solver.original_grid = copy.deepcopy(grid)
        return True
    
    def solve_puzzle(self):
        """Solve the current puzzle"""
        if not any(any(row) for row in self.solver.grid):
            print("❌ No puzzle loaded. Please load or input a puzzle first.")
            return
        
        if not self.solver.is_valid_puzzle(self.solver.grid):
            print("❌ Invalid puzzle! The puzzle has conflicts.")
            return
        
        print("\n🔍 Solving puzzle...")
        print("=" * 30)
        
        # Show original puzzle
        print("📋 Original puzzle:")
        self.print_grid(self.solver.original_grid)
        
        # Solve
        start_time = time.time()
        success = self.solver.solve_sudoku()
        solve_time = time.time() - start_time
        
        if success:
            print(f"\n✅ Puzzle solved successfully!")
            print(f"⏱️  Solve time: {solve_time:.4f} seconds")
            print("\n🎉 Solution:")
            self.print_colored_grid(self.solver.grid)
            
            # Show statistics
            stats = self.solver.get_statistics(self.solver.original_grid)
            print(f"\n📊 Puzzle Statistics:")
            print(f"   • Difficulty: {stats['difficulty']}")
            print(f"   • Original clues: {stats['filled']}/81")
            print(f"   • Cells solved: {stats['empty']}")
            print(f"   • Completion rate: {stats['completion']}%")
            
        else:
            print("❌ No solution found for this puzzle!")
    
    def solve_with_animation(self):
        """Solve puzzle with step-by-step animation"""
        if not any(any(row) for row in self.solver.grid):
            print("❌ No puzzle loaded. Please load or input a puzzle first.")
            return
        
        print("\n🎬 Solving with animation...")
        print("=" * 35)
        
        # Solve with step recording
        success = self.solver.solve_sudoku(record_steps=True)
        
        if not success:
            print("❌ No solution found!")
            return
        
        # Reset to original and animate
        self.solver.grid = copy.deepcopy(self.solver.original_grid)
        
        print("📋 Starting animation (Press Enter to continue each step)...")
        input("Press Enter to start...")
        
        for i, (row, col, num, action) in enumerate(self.solver.solution_steps):
            if action == 'place':
                self.solver.grid[row][col] = num
                print(f"\n🔹 Step {i+1}: Place {num} at ({row+1},{col+1})")
            elif action == 'backtrack':
                self.solver.grid[row][col] = 0
                print(f"\n🔸 Step {i+1}: Backtrack from ({row+1},{col+1})")
            
            self.print_grid(self.solver.grid)
            
            if i < len(self.solver.solution_steps) - 1:
                input("Press Enter for next step...")
        
        print("\n🎉 Animation complete!")
    
    def validate_puzzle(self):
        """Validate the current puzzle"""
        if not any(any(row) for row in self.solver.grid):
            print("❌ No puzzle loaded. Please load or input a puzzle first.")
            return
        
        print("\n🔍 Validating puzzle...")
        print("=" * 30)
        
        # Check for conflicts
        if not self.solver.is_valid_puzzle(self.solver.grid):
            print("❌ Invalid puzzle! There are conflicts in the current grid.")
            return
        
        # Check if solvable
        test_grid = copy.deepcopy(self.solver.grid)
        if self.solver.solve_sudoku(test_grid):
            print("✅ Puzzle is valid and solvable!")
            
            # Check for unique solution
            if self.solver.has_unique_solution(self.solver.grid):
                print("✅ Puzzle has a unique solution!")
            else:
                print("⚠️  Puzzle may have multiple solutions!")
        else:
            print("❌ Puzzle is invalid - no solution exists!")
    
    def show_statistics(self):
        """Show detailed statistics about the current puzzle"""
        if not any(any(row) for row in self.solver.grid):
            print("❌ No puzzle loaded. Please load or input a puzzle first.")
            return
        
        stats = self.solver.get_statistics(self.solver.grid)
        
        print("\n📊 Puzzle Statistics")
        print("=" * 30)
        print(f"📋 Filled cells: {stats['filled']}/81")
        print(f"🔳 Empty cells: {stats['empty']}")
        print(f"📈 Completion: {stats['completion']}%")
        print(f"⭐ Difficulty: {stats['difficulty']}")
        print(f"✅ Valid: {'Yes' if self.solver.is_valid_puzzle(self.solver.grid) else 'No'}")
        
        # Show difficulty breakdown
        print(f"\n💡 Difficulty Scale:")
        print(f"   Easy: ≤40 empty cells")
        print(f"   Medium: 41-50 empty cells")
        print(f"   Hard: 51-60 empty cells")
        print(f"   Expert: >60 empty cells")
    
    def load_puzzles(self):
        """Load saved puzzles from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.saved_puzzles = json.load(f)
            else:
                self.saved_puzzles = {}
        except Exception as e:
            print(f"Error loading puzzles: {e}")
            self.saved_puzzles = {}
    
    def save_puzzles(self):
        """Save puzzles to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.saved_puzzles, f, indent=2)
        except Exception as e:
            print(f"Error saving puzzles: {e}")
    
    def save_current_puzzle(self):
        """Save the current puzzle"""
        if not any(any(row) for row in self.solver.grid):
            print("❌ No puzzle loaded to save.")
            return
        
        name = input("Enter name for this puzzle: ").strip()
        if not name:
            print("❌ Invalid name.")
            return
        
        stats = self.solver.get_statistics(self.solver.grid)
        
        self.saved_puzzles[name] = {
            'grid': copy.deepcopy(self.solver.grid),
            'original_grid': copy.deepcopy(self.solver.original_grid),
            'difficulty': stats['difficulty'],
            'created': datetime.now().isoformat(),
            'statistics': stats
        }
        
        self.save_puzzles()
        print(f"✅ Puzzle '{name}' saved successfully!")
    
    def load_saved_puzzle(self):
        """Load a saved puzzle"""
        if not self.saved_puzzles:
            print("❌ No saved puzzles found.")
            return
        
        print("\n📁 Saved Puzzles:")
        print("=" * 25)
        
        puzzles = list(self.saved_puzzles.keys())
        for i, name in enumerate(puzzles, 1):
            puzzle = self.saved_puzzles[name]
            print(f"{i}. {name} ({puzzle['difficulty']})")
        
        try:
            choice = int(input(f"\nEnter puzzle number (1-{len(puzzles)}): ")) - 1
            if 0 <= choice < len(puzzles):
                name = puzzles[choice]
                puzzle = self.saved_puzzles[name]
                
                self.solver.grid = copy.deepcopy(puzzle['grid'])
                self.solver.original_grid = copy.deepcopy(puzzle['original_grid'])
                
                print(f"✅ Loaded puzzle '{name}'")
                self.print_grid(self.solver.grid)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Invalid input.")
    
    def load_example_puzzles(self):
        """Load example puzzles"""
        examples = {
            "Easy Example": [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ],
            "Medium Example": [
                [0, 0, 0, 6, 0, 0, 4, 0, 0],
                [7, 0, 0, 0, 0, 3, 6, 0, 0],
                [0, 0, 0, 0, 9, 1, 0, 8, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 0, 1, 8, 0, 0, 0, 3],
                [0, 0, 0, 3, 0, 6, 0, 4, 5],
                [0, 4, 0, 2, 0, 0, 0, 6, 0],
                [9, 0, 3, 0, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 1, 0, 0]
            ],
            "Hard Example": [
                [0, 0, 0, 0, 0, 0, 0, 1, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 6, 0, 2],
                [0, 0, 0, 0, 0, 3, 0, 7, 0],
                [5, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 4, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }
        
        print("\n🎲 Example Puzzles:")
        print("=" * 25)
        
        example_names = list(examples.keys())
        for i, name in enumerate(example_names, 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input(f"\nEnter example number (1-{len(example_names)}): ")) - 1
            if 0 <= choice < len(example_names):
                name = example_names[choice]
                grid = examples[name]
                
                self.solver.grid = copy.deepcopy(grid)
                self.solver.original_grid = copy.deepcopy(grid)
                
                print(f"✅ Loaded {name}")
                self.print_grid(self.solver.grid)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Invalid input.")
    
    def export_puzzle(self):
        """Export puzzle to file"""
        if not any(any(row) for row in self.solver.grid):
            print("❌ No puzzle loaded to export.")
            return
        
        filename = input("Enter filename (without extension): ").strip()
        if not filename:
            print("❌ Invalid filename.")
            return
        
        try:
            # Export as JSON
            data = {
                'grid': self.solver.grid,
                'original_grid': self.solver.original_grid,
                'exported': datetime.now().isoformat(),
                'statistics': self.solver.get_statistics(self.solver.grid)
            }
            
            with open(f"{filename}.json", 'w') as f:
                json.dump(data, f, indent=2)
            
            # Export as text
            with open(f"{filename}.txt", 'w') as f:
                f.write("Sudoku Puzzle\n")
                f.write("=" * 15 + "\n\n")
                for row in self.solver.grid:
                    f.write(' '.join(str(cell) if cell != 0 else '.' for cell in row) + '\n')
            
            print(f"✅ Puzzle exported as {filename}.json and {filename}.txt")
            
        except Exception as e:
            print(f"❌ Error exporting puzzle: {e}")
    
    def import_puzzle(self):
        """Import puzzle from file"""
        filename = input("Enter filename (with extension): ").strip()
        if not filename:
            print("❌ Invalid filename.")
            return
        
        try:
            if filename.endswith('.json'):
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.solver.grid = data['grid']
                    self.solver.original_grid = data.get('original_grid', copy.deepcopy(data['grid']))
            
            elif filename.endswith('.txt'):
                with open(filename, 'r') as f:
                    lines = f.readlines()
                    grid = []
                    for line in lines:
                        line = line.strip()
                        if len(line) >= 9:
                            row = []
                            for char in line.replace(' ', ''):
                                if char.isdigit():
                                    row.append(int(char))
                                elif char == '.':
                                    row.append(0)
                                if len(row) == 9:
                                    break
                            if len(row) == 9:
                                grid.append(row)
                            if len(grid) == 9:
                                break
                    
                    if len(grid) == 9:
                        self.solver.grid = grid
                        self.solver.original_grid = copy.deepcopy(grid)
                    else:
                        print("❌ Invalid file format.")
                        return
            
            else:
                print("❌ Unsupported file format. Use .json or .txt files.")
                return
            
            print(f"✅ Puzzle imported from {filename}")
            self.print_grid(self.solver.grid)
            
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found.")
        except Exception as e:
            print(f"❌ Error importing puzzle: {e}")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🧩 Sudoku Solver CLI - Help Guide
================================

Main Menu Options:
1. 📝 Input Puzzle - Enter your own puzzle
2. 🔍 Solve Puzzle - Solve the current puzzle
3. 🎬 Solve with Animation - See step-by-step solution
4. ✅ Validate Puzzle - Check if puzzle is valid
5. 📊 Show Statistics - View puzzle information
6. 💾 Save Puzzle - Save current puzzle
7. 📁 Load Saved Puzzle - Load previously saved puzzle
8. 🎲 Load Example - Load example puzzles
9. 📤 Export Puzzle - Export to file
10. 📥 Import Puzzle - Import from file
11. ❓ Help - Show this help
12. 🚪 Exit - Exit the program

Input Methods:
• Row by row: Enter 9 numbers for each row
• Cell by cell: Enter row col value (e.g., 1 1 5)
• Use 0 or . for empty cells

File Formats:
• JSON: Complete puzzle data with metadata
• TXT: Simple text format with numbers and dots

Tips:
• Original numbers are shown in blue
• Solved numbers are shown in red
• Validate puzzles before solving
• Save interesting puzzles for later
• Use animation to understand the algorithm

Algorithm:
The solver uses backtracking algorithm:
1. Find empty cell
2. Try numbers 1-9
3. Check if valid (row, column, box)
4. If valid, move to next cell
5. If no valid number, backtrack
6. Repeat until solved or no solution
        """
        print(help_text)
    
    def run(self):
        """Main program loop"""
        print("🧩 Welcome to Sudoku Solver CLI!")
        print("=" * 40)
        
        while True:
            print("\n📞 SUDOKU SOLVER")
            print("=" * 20)
            print("1. 📝 Input Puzzle")
            print("2. 🔍 Solve Puzzle")
            print("3. 🎬 Solve with Animation")
            print("4. ✅ Validate Puzzle")
            print("5. 📊 Show Statistics")
            print("6. 💾 Save Puzzle")
            print("7. 📁 Load Saved Puzzle")
            print("8. 🎲 Load Example")
            print("9. 📤 Export Puzzle")
            print("10. 📥 Import Puzzle")
            print("11. ❓ Help")
            print("12. 🚪 Exit")
            print("=" * 20)
            
            try:
                choice = input("👉 Enter your choice (1-12): ").strip()
                
                if choice == '1':
                    self.input_puzzle()
                elif choice == '2':
                    self.solve_puzzle()
                elif choice == '3':
                    self.solve_with_animation()
                elif choice == '4':
                    self.validate_puzzle()
                elif choice == '5':
                    self.show_statistics()
                elif choice == '6':
                    self.save_current_puzzle()
                elif choice == '7':
                    self.load_saved_puzzle()
                elif choice == '8':
                    self.load_example_puzzles()
                elif choice == '9':
                    self.export_puzzle()
                elif choice == '10':
                    self.import_puzzle()
                elif choice == '11':
                    self.show_help()
                elif choice == '12':
                    print("\n👋 Thank you for using Sudoku Solver!")
                    print("💾 All puzzles have been saved automatically.")
                    break
                else:
                    print("❌ Invalid choice. Please enter a number between 1-12.")
                
                if choice != '12':
                    input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    app = SudokuCLI()
    app.run()
