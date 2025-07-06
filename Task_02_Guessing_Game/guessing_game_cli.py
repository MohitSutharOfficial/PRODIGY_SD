"""
Number Guessing Game - Command Line Version
A fun command-line game where you try to guess a randomly generated number.
"""

import random
import time

class NumberGuessingGameCLI:
    def __init__(self):
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.min_range = 1
        self.max_range = 100
        self.game_active = False
        self.guess_history = []
        self.hint_used = False
        
    def display_welcome(self):
        """Display welcome message and game rules"""
        print("\n" + "="*60)
        print("🎯 WELCOME TO THE NUMBER GUESSING GAME! 🎯")
        print("="*60)
        print("🎮 How to Play:")
        print("• I'll think of a number within your chosen range")
        print("• You guess the number, and I'll tell you if it's too high or low")
        print("• Try to guess it in as few attempts as possible!")
        print("• You can type 'hint' for a clue or 'quit' to exit")
        print("="*60)
    
    def get_difficulty_settings(self):
        """Get game difficulty and range from user"""
        while True:
            print("\n🎚️  Choose Difficulty Level:")
            print("1. Easy (1-50) - 8 attempts")
            print("2. Medium (1-100) - 10 attempts")
            print("3. Hard (1-200) - 12 attempts")
            print("4. Expert (1-500) - 15 attempts")
            print("5. Custom Range")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.min_range, self.max_range = 1, 50
                self.max_attempts = 8
                break
            elif choice == '2':
                self.min_range, self.max_range = 1, 100
                self.max_attempts = 10
                break
            elif choice == '3':
                self.min_range, self.max_range = 1, 200
                self.max_attempts = 12
                break
            elif choice == '4':
                self.min_range, self.max_range = 1, 500
                self.max_attempts = 15
                break
            elif choice == '5':
                self.set_custom_range()
                break
            else:
                print("❌ Invalid choice! Please enter 1-5.")
    
    def set_custom_range(self):
        """Set custom range for the game"""
        while True:
            try:
                self.min_range = int(input("Enter minimum number: "))
                self.max_range = int(input("Enter maximum number: "))
                
                if self.min_range >= self.max_range:
                    print("❌ Maximum must be greater than minimum!")
                    continue
                
                if self.min_range < 1:
                    print("❌ Minimum must be at least 1!")
                    continue
                
                # Calculate max attempts based on range
                range_size = self.max_range - self.min_range + 1
                self.max_attempts = max(7, int(range_size.bit_length()) + 2)
                
                print(f"✅ Custom range set: {self.min_range}-{self.max_range}")
                print(f"🎯 You have {self.max_attempts} attempts")
                break
                
            except ValueError:
                print("❌ Please enter valid numbers!")
    
    def start_game(self):
        """Start a new game"""
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_active = True
        self.guess_history = []
        self.hint_used = False
        
        print(f"\n🎮 Game Started!")
        print(f"🔢 I'm thinking of a number between {self.min_range} and {self.max_range}")
        print(f"🎯 You have {self.max_attempts} attempts to guess it!")
        print(f"💡 Type 'hint' for a clue or 'quit' to exit")
        print("-" * 60)
    
    def get_user_guess(self):
        """Get and validate user's guess"""
        while True:
            user_input = input(f"\n🤔 Attempt {self.attempts + 1}/{self.max_attempts} - Enter your guess: ").strip().lower()
            
            if user_input == 'quit':
                return 'quit'
            elif user_input == 'hint':
                return 'hint'
            
            try:
                guess = int(user_input)
                
                if guess < self.min_range or guess > self.max_range:
                    print(f"❌ Please enter a number between {self.min_range} and {self.max_range}!")
                    continue
                
                return guess
                
            except ValueError:
                print("❌ Please enter a valid number, 'hint', or 'quit'!")
    
    def process_guess(self, guess):
        """Process the user's guess"""
        self.attempts += 1
        
        if guess == self.secret_number:
            self.win_game()
            return True
        elif guess < self.secret_number:
            feedback = "📈 Too Low! Try a higher number."
            self.guess_history.append(f"Attempt {self.attempts}: {guess} - Too Low")
        else:
            feedback = "📉 Too High! Try a lower number."
            self.guess_history.append(f"Attempt {self.attempts}: {guess} - Too High")
        
        print(f"\n{feedback}")
        
        # Show remaining attempts
        remaining = self.max_attempts - self.attempts
        if remaining > 0:
            print(f"🔄 {remaining} attempts remaining")
        
        # Check if max attempts reached
        if self.attempts >= self.max_attempts:
            self.lose_game()
            return True
        
        return False
    
    def give_hint(self):
        """Provide a hint to the user"""
        if self.hint_used:
            print("💡 You've already used your hint for this game!")
            return
        
        self.hint_used = True
        
        # Generate different types of hints
        hint_type = random.choice(['divisible', 'odd_even', 'digit_sum', 'range'])
        
        print("\n💡 Here's your hint:")
        
        if hint_type == 'divisible':
            for divisor in [2, 3, 5, 7]:
                if self.secret_number % divisor == 0:
                    hint = f"The number is divisible by {divisor}"
                    break
            else:
                hint = "The number is not divisible by 2, 3, 5, or 7"
        
        elif hint_type == 'odd_even':
            hint = f"The number is {'even' if self.secret_number % 2 == 0 else 'odd'}"
        
        elif hint_type == 'digit_sum':
            digit_sum = sum(int(digit) for digit in str(self.secret_number))
            hint = f"The sum of the digits is {digit_sum}"
        
        else:  # range hint
            quarter = (self.max_range - self.min_range) // 4
            if self.secret_number <= self.min_range + quarter:
                hint = "The number is in the lower quarter of the range"
            elif self.secret_number <= self.min_range + 2 * quarter:
                hint = "The number is in the second quarter of the range"
            elif self.secret_number <= self.min_range + 3 * quarter:
                hint = "The number is in the third quarter of the range"
            else:
                hint = "The number is in the upper quarter of the range"
        
        print(f"🔍 {hint}")
        self.guess_history.append(f"💡 Hint: {hint}")
    
    def win_game(self):
        """Handle game win"""
        self.game_active = False
        
        print("\n" + "🎉" * 20)
        print("🏆 CONGRATULATIONS! YOU WON! 🏆")
        print("🎉" * 20)
        print(f"✅ You guessed the number {self.secret_number} in {self.attempts} attempts!")
        
        # Calculate and display performance
        performance = self.get_performance_rating()
        print(f"🏅 Performance Rating: {performance}")
        
        # Show game statistics
        self.show_game_stats()
        
        # Celebration animation
        self.celebration_animation()
    
    def lose_game(self):
        """Handle game loss"""
        self.game_active = False
        
        print("\n" + "😞" * 20)
        print("💔 GAME OVER! 💔")
        print("😞" * 20)
        print(f"❌ You've used all {self.max_attempts} attempts!")
        print(f"🔢 The number was {self.secret_number}")
        
        # Show game statistics
        self.show_game_stats()
        
        print("\n💪 Don't give up! Try again and you'll do better!")
    
    def get_performance_rating(self):
        """Calculate performance rating based on attempts"""
        optimal_attempts = max(1, int((self.max_range - self.min_range + 1).bit_length()) - 1)
        
        if self.attempts <= optimal_attempts:
            return "🏆 Excellent! You're a master guesser!"
        elif self.attempts <= optimal_attempts + 2:
            return "🥇 Great! Outstanding performance!"
        elif self.attempts <= optimal_attempts + 4:
            return "🥈 Good! Nice guessing skills!"
        elif self.attempts <= self.max_attempts - 2:
            return "🥉 Fair! Keep practicing!"
        else:
            return "😅 Lucky! You made it just in time!"
    
    def show_game_stats(self):
        """Display game statistics"""
        print(f"\n📊 Game Statistics:")
        print(f"🎯 Target Number: {self.secret_number}")
        print(f"🔢 Range: {self.min_range} - {self.max_range}")
        print(f"🎮 Attempts Used: {self.attempts}/{self.max_attempts}")
        print(f"💡 Hint Used: {'Yes' if self.hint_used else 'No'}")
        
        if self.guess_history:
            print(f"\n📝 Guess History:")
            for entry in self.guess_history:
                print(f"  {entry}")
    
    def celebration_animation(self):
        """Display celebration animation"""
        print("\n🎊 Celebration Time! 🎊")
        celebration_frames = [
            "    🎉    🎉    🎉",
            "  🎊  🎉  🎊  🎉  🎊",
            "🎉  🎊  🎉  🎊  🎉  🎊",
            "  🎊  🎉  🎊  🎉  🎊",
            "    🎉    🎉    🎉"
        ]
        
        for _ in range(2):
            for frame in celebration_frames:
                print(f"\r{frame}", end="", flush=True)
                time.sleep(0.3)
        print("\n")
    
    def play_again(self):
        """Ask if user wants to play again"""
        while True:
            choice = input("\n🎮 Would you like to play again? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' for yes or 'n' for no.")
    
    def run(self):
        """Main game loop"""
        self.display_welcome()
        
        while True:
            try:
                self.get_difficulty_settings()
                self.start_game()
                
                # Game loop
                while self.game_active:
                    guess = self.get_user_guess()
                    
                    if guess == 'quit':
                        print("\n👋 Thanks for playing! Goodbye!")
                        return
                    elif guess == 'hint':
                        self.give_hint()
                        continue
                    
                    # Process the guess
                    if self.process_guess(guess):
                        break  # Game ended (won or lost)
                
                # Ask if user wants to play again
                if not self.play_again():
                    print("\n🎯 Thanks for playing the Number Guessing Game!")
                    print("👋 Hope you had fun! Come back anytime!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Thanks for playing!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("🔄 Restarting the game...")

def main():
    """Main function to run the guessing game"""
    game = NumberGuessingGameCLI()
    game.run()

if __name__ == "__main__":
    main()
