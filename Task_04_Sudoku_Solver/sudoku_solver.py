"""
Sudoku Solver - GUI Version
A comprehensive Sudoku solver with backtracking algorithm and interactive interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import time
import threading
from datetime import datetime
import copy

class SudokuSolver:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_steps = []
        self.solving = False
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
        if self.solving and hasattr(self, 'stop_solving') and self.stop_solving:
            return False
        
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

class SudokuGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver - Advanced")
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        
        self.solver = SudokuSolver()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.solving_animation = False
        
        self.setup_ui()
        self.load_sample_puzzle()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🧩 Sudoku Solver", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Create Sudoku grid
        self.create_sudoku_grid(main_frame)
        
        # Control buttons
        self.create_control_buttons(main_frame)
        
        # Status and info
        self.create_status_panel(main_frame)
        
        # Menu
        self.create_menu()
    
    def create_sudoku_grid(self, parent):
        """Create the 9x9 Sudoku grid"""
        grid_frame = ttk.Frame(parent, relief="solid", borderwidth=2)
        grid_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        for i in range(9):
            for j in range(9):
                # Create cell with appropriate borders for 3x3 blocks
                cell_frame = tk.Frame(grid_frame, bg='white', 
                                    highlightbackground='black', highlightthickness=1)
                
                # Thicker borders for 3x3 block separation
                padx = (3 if j % 3 == 0 else 1, 3 if j % 3 == 2 else 1)
                pady = (3 if i % 3 == 0 else 1, 3 if i % 3 == 2 else 1)
                
                cell_frame.grid(row=i, column=j, padx=padx, pady=pady)
                
                # Entry widget for each cell
                cell = tk.Entry(cell_frame, width=2, font=("Arial", 14, "bold"),
                               justify='center', bd=0, highlightthickness=0)
                cell.pack(padx=2, pady=2)
                
                # Bind events
                cell.bind('<KeyPress>', lambda e, r=i, c=j: self.on_key_press(e, r, c))
                cell.bind('<FocusIn>', lambda e, r=i, c=j: self.on_cell_focus(e, r, c))
                
                self.cells[i][j] = cell
    
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Row 1 buttons
        row1_frame = ttk.Frame(button_frame)
        row1_frame.pack(pady=5)
        
        self.solve_btn = ttk.Button(row1_frame, text="🔍 Solve", 
                                   command=self.solve_puzzle, width=12)
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(row1_frame, text="🗑️ Clear", 
                                   command=self.clear_grid, width=12)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.validate_btn = ttk.Button(row1_frame, text="✅ Validate", 
                                      command=self.validate_puzzle, width=12)
        self.validate_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 2 buttons
        row2_frame = ttk.Frame(button_frame)
        row2_frame.pack(pady=5)
        
        self.load_btn = ttk.Button(row2_frame, text="📁 Load", 
                                  command=self.load_puzzle, width=12)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(row2_frame, text="💾 Save", 
                                  command=self.save_puzzle, width=12)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.example_btn = ttk.Button(row2_frame, text="🎲 Examples", 
                                     command=self.show_examples, width=12)
        self.example_btn.pack(side=tk.LEFT, padx=5)
    
    def create_status_panel(self, parent):
        """Create status and information panel"""
        status_frame = ttk.LabelFrame(parent, text="Status & Information", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready to solve puzzles!")
        self.status_label.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Info labels
        info_frame = ttk.Frame(status_frame)
        info_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.difficulty_label = ttk.Label(info_frame, text="Difficulty: -")
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = ttk.Label(info_frame, text="Solve Time: -")
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.filled_label = ttk.Label(info_frame, text="Filled: 0/81")
        self.filled_label.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Puzzle", command=self.clear_grid)
        file_menu.add_command(label="Load Puzzle", command=self.load_puzzle)
        file_menu.add_command(label="Save Puzzle", command=self.save_puzzle)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Solve menu
        solve_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Solve", menu=solve_menu)
        solve_menu.add_command(label="Solve Instantly", command=self.solve_puzzle)
        solve_menu.add_command(label="Solve with Animation", command=self.solve_with_animation)
        solve_menu.add_command(label="Validate Puzzle", command=self.validate_puzzle)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Use", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
    
    def on_key_press(self, event, row, col):
        """Handle key press in cell"""
        if event.char.isdigit() and event.char != '0':
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, event.char)
            self.update_grid_from_ui()
            self.update_status()
            return "break"
        elif event.keysym in ['BackSpace', 'Delete']:
            self.cells[row][col].delete(0, tk.END)
            self.update_grid_from_ui()
            self.update_status()
            return "break"
        else:
            return "break"
    
    def on_cell_focus(self, event, row, col):
        """Handle cell focus"""
        self.highlight_related_cells(row, col)
    
    def highlight_related_cells(self, row, col):
        """Highlight cells in same row, column, and 3x3 box"""
        # Reset all cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].configure(bg='white')
        
        # Highlight current cell
        self.cells[row][col].configure(bg='lightblue')
        
        # Highlight row and column
        for i in range(9):
            if i != row:
                self.cells[i][col].configure(bg='lightgray')
        for j in range(9):
            if j != col:
                self.cells[row][j].configure(bg='lightgray')
        
        # Highlight 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if i != row or j != col:
                    self.cells[i][j].configure(bg='lightyellow')
    
    def update_grid_from_ui(self):
        """Update internal grid from UI"""
        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    self.solver.grid[i][j] = int(value)
                else:
                    self.solver.grid[i][j] = 0
    
    def update_ui_from_grid(self):
        """Update UI from internal grid"""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if self.solver.grid[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.solver.grid[i][j]))
                    # Color original numbers differently
                    if self.solver.original_grid[i][j] != 0:
                        self.cells[i][j].configure(fg='blue', font=("Arial", 14, "bold"))
                    else:
                        self.cells[i][j].configure(fg='red', font=("Arial", 14, "normal"))
    
    def update_status(self):
        """Update status information"""
        filled = sum(row.count(0) for row in self.solver.grid)
        filled = 81 - filled
        
        self.filled_label.config(text=f"Filled: {filled}/81")
        
        if filled > 0:
            difficulty = self.solver.get_difficulty_level(self.solver.grid)
            self.difficulty_label.config(text=f"Difficulty: {difficulty}")
        else:
            self.difficulty_label.config(text="Difficulty: -")
        
        # Update progress bar
        progress = (filled / 81) * 100
        self.progress_var.set(progress)
    
    def solve_puzzle(self):
        """Solve the current puzzle"""
        self.update_grid_from_ui()
        
        if not self.solver.is_valid_puzzle(self.solver.grid):
            messagebox.showerror("Error", "Invalid puzzle! Please check for conflicts.")
            return
        
        self.status_label.config(text="Solving puzzle...")
        self.solve_btn.config(state='disabled')
        self.root.update()
        
        # Store original grid
        self.solver.original_grid = copy.deepcopy(self.solver.grid)
        
        # Solve in separate thread
        def solve_thread():
            success = self.solver.solve_sudoku()
            self.root.after(0, self.solve_completed, success)
        
        threading.Thread(target=solve_thread, daemon=True).start()
    
    def solve_completed(self, success):
        """Handle solve completion"""
        if success:
            self.update_ui_from_grid()
            self.status_label.config(text=f"Puzzle solved! Time: {self.solver.solve_time:.3f}s")
            self.time_label.config(text=f"Solve Time: {self.solver.solve_time:.3f}s")
            self.update_status()
            messagebox.showinfo("Success", f"Puzzle solved successfully!\nTime: {self.solver.solve_time:.3f} seconds")
        else:
            self.status_label.config(text="No solution found!")
            messagebox.showerror("Error", "This puzzle has no solution!")
        
        self.solve_btn.config(state='normal')
    
    def solve_with_animation(self):
        """Solve puzzle with step-by-step animation"""
        self.update_grid_from_ui()
        
        if not self.solver.is_valid_puzzle(self.solver.grid):
            messagebox.showerror("Error", "Invalid puzzle! Please check for conflicts.")
            return
        
        self.status_label.config(text="Solving with animation...")
        self.solving_animation = True
        
        # Store original grid
        self.solver.original_grid = copy.deepcopy(self.solver.grid)
        
        # Solve with step recording
        def solve_animated():
            success = self.solver.solve_sudoku(record_steps=True)
            if success:
                self.root.after(0, self.animate_solution)
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No solution found!"))
        
        threading.Thread(target=solve_animated, daemon=True).start()
    
    def animate_solution(self):
        """Animate the solution steps"""
        if not self.solver.solution_steps:
            return
        
        # Reset to original grid
        self.solver.grid = copy.deepcopy(self.solver.original_grid)
        self.update_ui_from_grid()
        
        def animate_step(step_index):
            if step_index >= len(self.solver.solution_steps):
                self.solving_animation = False
                self.status_label.config(text="Animation complete!")
                return
            
            row, col, num, action = self.solver.solution_steps[step_index]
            
            if action == 'place':
                self.solver.grid[row][col] = num
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].insert(0, str(num))
                self.cells[row][col].configure(bg='lightgreen')
            elif action == 'backtrack':
                self.solver.grid[row][col] = 0
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].configure(bg='lightcoral')
            
            # Continue animation
            self.root.after(50, lambda: animate_step(step_index + 1))
        
        animate_step(0)
    
    def validate_puzzle(self):
        """Validate the current puzzle"""
        self.update_grid_from_ui()
        
        if not self.solver.is_valid_puzzle(self.solver.grid):
            messagebox.showerror("Invalid", "This puzzle has conflicts!")
            return
        
        # Check if it's solvable
        test_grid = copy.deepcopy(self.solver.grid)
        if self.solver.solve_sudoku(test_grid):
            messagebox.showinfo("Valid", "This puzzle is valid and solvable!")
        else:
            messagebox.showerror("Invalid", "This puzzle has no solution!")
    
    def clear_grid(self):
        """Clear the entire grid"""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].configure(bg='white', fg='black', font=("Arial", 14, "normal"))
        
        self.solver.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solver.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.update_status()
        self.status_label.config(text="Grid cleared!")
    
    def load_puzzle(self):
        """Load puzzle from file"""
        filename = filedialog.askopenfilename(
            title="Load Sudoku Puzzle",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'r') as f:
                        data = json.load(f)
                        self.solver.grid = data['grid']
                else:
                    # Load from text file
                    with open(filename, 'r') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines[:9]):
                            for j, char in enumerate(line.strip().replace(' ', '')[:9]):
                                if char.isdigit():
                                    self.solver.grid[i][j] = int(char)
                                else:
                                    self.solver.grid[i][j] = 0
                
                self.solver.original_grid = copy.deepcopy(self.solver.grid)
                self.update_ui_from_grid()
                self.update_status()
                self.status_label.config(text=f"Loaded puzzle from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load puzzle: {str(e)}")
    
    def save_puzzle(self):
        """Save current puzzle to file"""
        self.update_grid_from_ui()
        
        filename = filedialog.asksaveasfilename(
            title="Save Sudoku Puzzle",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    data = {
                        'grid': self.solver.grid,
                        'difficulty': self.solver.get_difficulty_level(self.solver.grid),
                        'created': datetime.now().isoformat()
                    }
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                else:
                    # Save as text file
                    with open(filename, 'w') as f:
                        for row in self.solver.grid:
                            f.write(' '.join(str(cell) if cell != 0 else '.' for cell in row) + '\n')
                
                self.status_label.config(text=f"Saved puzzle to {filename}")
                messagebox.showinfo("Success", f"Puzzle saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save puzzle: {str(e)}")
    
    def show_examples(self):
        """Show example puzzles"""
        examples = {
            "Easy": [
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
            "Medium": [
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
            "Hard": [
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
        
        example_window = tk.Toplevel(self.root)
        example_window.title("Example Puzzles")
        example_window.geometry("300x200")
        
        ttk.Label(example_window, text="Choose an example puzzle:", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        for difficulty, grid in examples.items():
            btn = ttk.Button(example_window, text=f"{difficulty} Puzzle",
                           command=lambda g=grid: self.load_example(g, example_window))
            btn.pack(pady=5)
        
        ttk.Button(example_window, text="Cancel", 
                  command=example_window.destroy).pack(pady=10)
    
    def load_example(self, grid, window):
        """Load an example puzzle"""
        self.solver.grid = copy.deepcopy(grid)
        self.solver.original_grid = copy.deepcopy(grid)
        self.update_ui_from_grid()
        self.update_status()
        self.status_label.config(text="Example puzzle loaded!")
        window.destroy()
    
    def load_sample_puzzle(self):
        """Load a sample puzzle on startup"""
        sample_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        self.solver.grid = copy.deepcopy(sample_grid)
        self.solver.original_grid = copy.deepcopy(sample_grid)
        self.update_ui_from_grid()
        self.update_status()
        self.status_label.config(text="Sample puzzle loaded - ready to solve!")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🧩 Sudoku Solver Help

How to use:
1. Enter numbers 1-9 in the grid cells
2. Use backspace/delete to clear cells
3. Click 'Solve' to find the solution
4. Use 'Validate' to check if puzzle is valid
5. Load/Save puzzles using the file menu

Features:
• Instant solving with backtracking algorithm
• Animated solving to see the process
• Puzzle validation and conflict detection
• Multiple difficulty levels
• Import/Export functionality
• Example puzzles included

Tips:
• Blue numbers are original clues
• Red numbers are solved values
• Related cells are highlighted when focused
• The difficulty is estimated automatically
        """
        
        messagebox.showinfo("Help", help_text)
    
    def show_about(self):
        """Show about information"""
        about_text = """
🧩 Sudoku Solver v1.0

A comprehensive Sudoku solving application with:
• Advanced backtracking algorithm
• Interactive GUI with visual feedback
• Animation capabilities
• Puzzle validation and generation
• Import/Export functionality

Created for PRODIGY Software Development Internship
Task 4: Sudoku Solver Implementation

© 2025 - Educational Project
        """
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SudokuGUI()
    app.run()
