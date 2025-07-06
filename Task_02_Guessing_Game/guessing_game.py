import tkinter as tk
from tkinter import ttk, messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("500x450")
        self.root.configure(bg='#f0f8ff')
        
        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.min_range = 1
        self.max_range = 100
        self.game_active = False
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎯 Number Guessing Game", 
            font=("Arial", 20, "bold"),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Game settings frame
        settings_frame = tk.LabelFrame(
            main_frame, 
            text="Game Settings", 
            font=("Arial", 12, "bold"),
            bg='#f0f8ff',
            fg='#34495e',
            padx=10,
            pady=10
        )
        settings_frame.pack(fill='x', pady=10)
        
        # Difficulty selection
        tk.Label(
            settings_frame, 
            text="Difficulty Level:", 
            font=("Arial", 10),
            bg='#f0f8ff'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.difficulty_var = tk.StringVar(value="Medium")
        self.difficulty_combo = ttk.Combobox(
            settings_frame, 
            textvariable=self.difficulty_var,
            values=["Easy (1-50)", "Medium (1-100)", "Hard (1-200)", "Expert (1-500)"],
            state="readonly",
            font=("Arial", 10),
            width=15
        )
        self.difficulty_combo.grid(row=0, column=1, padx=10, pady=5)
        self.difficulty_combo.bind('<<ComboboxSelected>>', self.on_difficulty_change)
        
        # Custom range option
        tk.Label(
            settings_frame, 
            text="Custom Range:", 
            font=("Arial", 10),
            bg='#f0f8ff'
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        range_frame = tk.Frame(settings_frame, bg='#f0f8ff')
        range_frame.grid(row=1, column=1, padx=10, pady=5)
        
        self.min_entry = tk.Entry(range_frame, font=("Arial", 10), width=8)
        self.min_entry.pack(side='left')
        self.min_entry.insert(0, "1")
        
        tk.Label(range_frame, text=" to ", font=("Arial", 10), bg='#f0f8ff').pack(side='left')
        
        self.max_entry = tk.Entry(range_frame, font=("Arial", 10), width=8)
        self.max_entry.pack(side='left')
        self.max_entry.insert(0, "100")
        
        # Start game button
        self.start_btn = tk.Button(
            settings_frame,
            text="🎮 Start New Game",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=self.start_game
        )
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Game play frame
        self.game_frame = tk.LabelFrame(
            main_frame, 
            text="Game Play", 
            font=("Arial", 12, "bold"),
            bg='#f0f8ff',
            fg='#34495e',
            padx=10,
            pady=10
        )
        self.game_frame.pack(fill='both', expand=True, pady=10)
        
        # Game info
        self.info_label = tk.Label(
            self.game_frame, 
            text="Click 'Start New Game' to begin!", 
            font=("Arial", 11),
            bg='#f0f8ff',
            fg='#7f8c8d'
        )
        self.info_label.pack(pady=10)
        
        # Guess input
        guess_frame = tk.Frame(self.game_frame, bg='#f0f8ff')
        guess_frame.pack(pady=10)
        
        tk.Label(
            guess_frame, 
            text="Your Guess:", 
            font=("Arial", 11),
            bg='#f0f8ff'
        ).pack(side='left', padx=5)
        
        self.guess_entry = tk.Entry(
            guess_frame, 
            font=("Arial", 12), 
            width=10,
            state='disabled'
        )
        self.guess_entry.pack(side='left', padx=5)
        self.guess_entry.bind('<Return>', self.make_guess)
        
        self.guess_btn = tk.Button(
            guess_frame,
            text="🎯 Guess",
            font=("Arial", 10, "bold"),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.make_guess,
            state='disabled'
        )
        self.guess_btn.pack(side='left', padx=5)
        
        # Feedback area
        self.feedback_label = tk.Label(
            self.game_frame, 
            text="", 
            font=("Arial", 12, "bold"),
            bg='#f0f8ff',
            fg='#e74c3c'
        )
        self.feedback_label.pack(pady=10)
        
        # Statistics
        self.stats_label = tk.Label(
            self.game_frame, 
            text="", 
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#34495e'
        )
        self.stats_label.pack(pady=5)
        
        # Guess history
        self.history_frame = tk.Frame(self.game_frame, bg='#f0f8ff')
        self.history_frame.pack(pady=10, fill='both', expand=True)
        
        tk.Label(
            self.history_frame, 
            text="Guess History:", 
            font=("Arial", 10, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        self.history_text = tk.Text(
            self.history_frame, 
            height=6, 
            font=("Arial", 9),
            bg='#ffffff',
            fg='#2c3e50',
            state='disabled'
        )
        self.history_text.pack(fill='both', expand=True, pady=5)
        
        # Scroll bar for history
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        # Hint button
        self.hint_btn = tk.Button(
            self.game_frame,
            text="💡 Get Hint",
            font=("Arial", 10),
            bg='#f39c12',
            fg='white',
            cursor='hand2',
            command=self.give_hint,
            state='disabled'
        )
        self.hint_btn.pack(pady=5)
        
    def on_difficulty_change(self, event):
        """Handle difficulty level change"""
        difficulty = self.difficulty_var.get()
        
        if difficulty.startswith("Easy"):
            self.min_entry.delete(0, tk.END)
            self.min_entry.insert(0, "1")
            self.max_entry.delete(0, tk.END)
            self.max_entry.insert(0, "50")
        elif difficulty.startswith("Medium"):
            self.min_entry.delete(0, tk.END)
            self.min_entry.insert(0, "1")
            self.max_entry.delete(0, tk.END)
            self.max_entry.insert(0, "100")
        elif difficulty.startswith("Hard"):
            self.min_entry.delete(0, tk.END)
            self.min_entry.insert(0, "1")
            self.max_entry.delete(0, tk.END)
            self.max_entry.insert(0, "200")
        elif difficulty.startswith("Expert"):
            self.min_entry.delete(0, tk.END)
            self.min_entry.insert(0, "1")
            self.max_entry.delete(0, tk.END)
            self.max_entry.insert(0, "500")
    
    def start_game(self):
        """Start a new game"""
        try:
            self.min_range = int(self.min_entry.get())
            self.max_range = int(self.max_entry.get())
            
            if self.min_range >= self.max_range:
                messagebox.showerror("Invalid Range", "Maximum must be greater than minimum!")
                return
            
            if self.min_range < 1:
                messagebox.showerror("Invalid Range", "Minimum must be at least 1!")
                return
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for the range!")
            return
        
        # Generate secret number
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_active = True
        
        # Calculate max attempts based on range
        range_size = self.max_range - self.min_range + 1
        self.max_attempts = max(7, int(range_size.bit_length()) + 2)
        
        # Enable game controls
        self.guess_entry.config(state='normal')
        self.guess_btn.config(state='normal')
        self.hint_btn.config(state='normal')
        self.start_btn.config(text="🔄 New Game")
        
        # Update UI
        self.info_label.config(
            text=f"I'm thinking of a number between {self.min_range} and {self.max_range}!\nCan you guess it?",
            fg='#27ae60'
        )
        self.feedback_label.config(text="")
        self.stats_label.config(text=f"Attempts: 0 | Max Attempts: {self.max_attempts}")
        
        # Clear history
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state='disabled')
        
        # Clear guess entry
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        
        # Add game start to history
        self.add_to_history(f"🎮 New game started! Range: {self.min_range}-{self.max_range}")
    
    def make_guess(self, event=None):
        """Process user's guess"""
        if not self.game_active:
            return
        
        try:
            guess = int(self.guess_entry.get())
            
            if guess < self.min_range or guess > self.max_range:
                messagebox.showerror("Invalid Guess", f"Please enter a number between {self.min_range} and {self.max_range}!")
                return
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            return
        
        self.attempts += 1
        self.guess_entry.delete(0, tk.END)
        
        # Check guess
        if guess == self.secret_number:
            self.win_game()
        elif guess < self.secret_number:
            self.feedback_label.config(text="📈 Too Low! Try a higher number.", fg='#e74c3c')
            self.add_to_history(f"Attempt {self.attempts}: {guess} - Too Low! 📈")
        else:
            self.feedback_label.config(text="📉 Too High! Try a lower number.", fg='#e74c3c')
            self.add_to_history(f"Attempt {self.attempts}: {guess} - Too High! 📉")
        
        # Update stats
        self.stats_label.config(text=f"Attempts: {self.attempts} | Max Attempts: {self.max_attempts}")
        
        # Check if max attempts reached
        if self.attempts >= self.max_attempts and guess != self.secret_number:
            self.lose_game()
    
    def win_game(self):
        """Handle game win"""
        self.game_active = False
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        self.hint_btn.config(state='disabled')
        
        # Calculate performance
        performance = self.get_performance_rating()
        
        self.feedback_label.config(
            text=f"🎉 Congratulations! You guessed it in {self.attempts} attempts!", 
            fg='#27ae60'
        )
        
        self.add_to_history(f"🎉 WINNER! The number was {self.secret_number}")
        self.add_to_history(f"🏆 Performance: {performance}")
        
        # Show victory dialog
        messagebox.showinfo(
            "Congratulations! 🎉", 
            f"You guessed the number {self.secret_number} in {self.attempts} attempts!\n\n"
            f"Performance Rating: {performance}\n\n"
            "Would you like to play again?"
        )
    
    def lose_game(self):
        """Handle game loss"""
        self.game_active = False
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        self.hint_btn.config(state='disabled')
        
        self.feedback_label.config(
            text=f"😞 Game Over! The number was {self.secret_number}", 
            fg='#e74c3c'
        )
        
        self.add_to_history(f"😞 Game Over! The number was {self.secret_number}")
        self.add_to_history(f"💔 You used all {self.max_attempts} attempts")
        
        # Show game over dialog
        messagebox.showinfo(
            "Game Over! 😞", 
            f"You've used all {self.max_attempts} attempts!\n\n"
            f"The number was {self.secret_number}\n\n"
            "Better luck next time!"
        )
    
    def give_hint(self):
        """Provide a hint to the user"""
        if not self.game_active:
            return
        
        # Generate different types of hints
        hint_type = random.choice(['divisible', 'odd_even', 'digit_sum', 'range'])
        
        if hint_type == 'divisible':
            for divisor in [2, 3, 5, 7]:
                if self.secret_number % divisor == 0:
                    hint = f"💡 Hint: The number is divisible by {divisor}"
                    break
            else:
                hint = f"💡 Hint: The number is not divisible by 2, 3, 5, or 7"
        
        elif hint_type == 'odd_even':
            hint = f"💡 Hint: The number is {'even' if self.secret_number % 2 == 0 else 'odd'}"
        
        elif hint_type == 'digit_sum':
            digit_sum = sum(int(digit) for digit in str(self.secret_number))
            hint = f"💡 Hint: The sum of the digits is {digit_sum}"
        
        else:  # range hint
            quarter = (self.max_range - self.min_range) // 4
            if self.secret_number <= self.min_range + quarter:
                hint = f"💡 Hint: The number is in the lower quarter of the range"
            elif self.secret_number <= self.min_range + 2 * quarter:
                hint = f"💡 Hint: The number is in the second quarter of the range"
            elif self.secret_number <= self.min_range + 3 * quarter:
                hint = f"💡 Hint: The number is in the third quarter of the range"
            else:
                hint = f"💡 Hint: The number is in the upper quarter of the range"
        
        self.add_to_history(hint)
        self.feedback_label.config(text=hint, fg='#f39c12')
        
        # Disable hint button after use
        self.hint_btn.config(state='disabled')
    
    def get_performance_rating(self):
        """Calculate performance rating based on attempts"""
        optimal_attempts = max(1, int((self.max_range - self.min_range + 1).bit_length()) - 1)
        
        if self.attempts <= optimal_attempts:
            return "🏆 Excellent!"
        elif self.attempts <= optimal_attempts + 2:
            return "🥇 Great!"
        elif self.attempts <= optimal_attempts + 4:
            return "🥈 Good!"
        elif self.attempts <= self.max_attempts - 2:
            return "🥉 Fair"
        else:
            return "😅 Lucky!"
    
    def add_to_history(self, message):
        """Add message to history"""
        self.history_text.config(state='normal')
        self.history_text.insert(tk.END, message + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
