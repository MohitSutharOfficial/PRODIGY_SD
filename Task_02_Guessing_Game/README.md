# Number Guessing Game

**PRODIGY Software Development Internship - Task 2**

A fun and interactive number guessing game that challenges users to guess a randomly generated number within a specified range. This project includes both a GUI version and a command-line version, developed as part of the PRODIGY Software Development internship program.

## 🎯 Task Overview

**Task**: Create a Guessing Game  
**Objective**: Build a program that generates a random number and challenges the user to guess it  
**Requirements**: 
- Generate a random number
- Prompt user to input their guess
- Compare guess to generated number
- Provide feedback (too high/too low)
- Continue until correct guess
- Display number of attempts

## ✨ Implementation Features

This implementation exceeds the basic requirements by providing:
- **Dual Interface Support**: GUI and CLI versions
- **Multiple Difficulty Levels**: Easy, Medium, Hard, Expert, and Custom
- **Smart Attempt Limiting**: Based on range size using optimal algorithms
- **Hint System**: Provides clues when requested
- **Performance Rating**: Evaluates guessing efficiency
- **Game Statistics**: Tracks attempts and guess history
- **Visual Feedback**: Color-coded responses and animations

## 🎮 Game Features

### 🖥️ GUI Version (`guessing_game.py`)
- **Beautiful Interface**: Modern design with color-coded feedback
- **Difficulty Selection**: Pre-defined and custom difficulty levels
- **Real-time Statistics**: Live attempt counter and remaining attempts
- **Guess History**: Visual log of all attempts and feedback
- **Hint System**: One hint per game with different hint types
- **Performance Rating**: Evaluates your guessing skills
- **Victory Animations**: Celebration dialogs and feedback

### 💻 Command-Line Version (`guessing_game_cli.py`)
- **Interactive Interface**: Colorful terminal-based gameplay
- **Difficulty Options**: Multiple pre-set difficulty levels
- **Smart Hints**: Various hint types (divisibility, odd/even, digit sum, range)
- **Game Statistics**: Detailed performance analysis
- **Celebration Animation**: ASCII art celebrations
- **Guess History**: Complete log of all attempts

## 🎚️ Difficulty Levels

| Level | Range | Max Attempts | Description |
|-------|-------|--------------|-------------|
| Easy | 1-50 | 8 | Perfect for beginners |
| Medium | 1-100 | 10 | Standard difficulty |
| Hard | 1-200 | 12 | Challenging gameplay |
| Expert | 1-500 | 15 | For experienced players |
| Custom | User-defined | Auto-calculated | Set your own range |

## 🧠 Hint System

The game provides intelligent hints to help players:
- **Divisibility Hints**: "The number is divisible by X"
- **Odd/Even Hints**: "The number is odd/even"
- **Digit Sum Hints**: "The sum of digits is X"
- **Range Hints**: "The number is in the upper/lower quarter"

## 🏆 Performance Rating System

Based on the number of attempts relative to the optimal strategy:
- **🏆 Excellent**: Within optimal attempts (binary search efficiency)
- **🥇 Great**: 1-2 attempts above optimal
- **🥈 Good**: 3-4 attempts above optimal
- **🥉 Fair**: 5+ attempts above optimal
- **😅 Lucky**: Made it just in time!

## 📋 Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python installation)

## 🚀 Installation & Usage

### Quick Start (Windows)
```bash
# Navigate to the task folder
cd Task_02_Guessing_Game

# Use the launcher
run_game.bat
```

### Manual Installation
```bash
# Clone the repository
git clone <repository-url>
cd PRODIGY_SD/Task_02_Guessing_Game

# Run GUI version
python guessing_game.py

# Run CLI version
python guessing_game_cli.py

# Run tests
python test_demo.py
```

## 🎮 How to Play

### GUI Version
1. Launch the application
2. Choose difficulty level or set custom range
3. Click "Start New Game"
4. Enter your guess and click "Guess"
5. Follow the feedback (too high/too low)
6. Use the hint button if needed
7. Keep guessing until you find the number!

### Command-Line Version
1. Run the CLI version
2. Choose difficulty level (1-5)
3. Enter your guesses when prompted
4. Type 'hint' for a clue
5. Type 'quit' to exit
6. Try to guess the number in minimum attempts!

## 🧪 Testing and Validation

The project includes comprehensive testing:

### Automated Test Suite
```bash
python test_demo.py
```

**Test Coverage:**
- ✅ Random number generation validation
- ✅ Guess validation logic
- ✅ Performance rating calculation
- ✅ Game simulation with optimal strategy
- ✅ All game mechanics verification

### Manual Testing
Both versions tested for:
- Range validation
- Input validation
- Hint system accuracy
- Performance calculations
- User interface responsiveness

## 📊 Technical Implementation

### Key Algorithms:
1. **Optimal Attempts Calculation**: Uses bit length of range for smart attempt limiting
2. **Binary Search Simulation**: Demonstrates optimal guessing strategy
3. **Hint Generation**: Multiple hint types with randomization
4. **Performance Analysis**: Compares user performance to optimal strategy

### Code Structure:
- **Object-Oriented Design**: Clean, maintainable code structure
- **Error Handling**: Comprehensive input validation and error recovery
- **User Experience**: Intuitive interfaces with clear feedback
- **Documentation**: Well-commented code with docstrings

## 📁 File Structure

```
Task_02_Guessing_Game/
├── guessing_game.py          # GUI version (tkinter-based)
├── guessing_game_cli.py      # Command-line version
├── test_demo.py              # Test suite and demo launcher
├── run_game.bat              # Windows batch launcher
├── requirements.txt          # Project dependencies
└── README.md                 # This documentation
```

## 🎯 Example Gameplay

### Sample Game Session:
```
🎮 Game Started!
🔢 I'm thinking of a number between 1 and 100
🎯 You have 10 attempts to guess it!

🤔 Attempt 1/10 - Enter your guess: 50
📉 Too High! Try a lower number.
🔄 9 attempts remaining

🤔 Attempt 2/10 - Enter your guess: 25
📈 Too Low! Try a higher number.
🔄 8 attempts remaining

🤔 Attempt 3/10 - Enter your guess: hint
💡 Here's your hint:
🔍 The number is even

🤔 Attempt 3/10 - Enter your guess: 38
🎉 Congratulations! You guessed it in 3 attempts!
🏅 Performance Rating: 🥇 Great! Outstanding performance!
```

## 🚀 Advanced Features

### Beyond Basic Requirements:
1. **Multiple Difficulty Levels**: 5 different challenge levels
2. **Smart Attempt Limiting**: Calculated based on range size
3. **Intelligent Hint System**: 4 different hint types
4. **Performance Analysis**: Compares to optimal strategy
5. **Dual Interface**: Both GUI and CLI versions
6. **Game Statistics**: Comprehensive tracking and analysis
7. **Visual Feedback**: Colors, animations, and celebrations
8. **Robust Testing**: Automated test suite with multiple scenarios

## 📊 Project Statistics

- **Lines of Code**: ~900+ lines
- **Files Created**: 5 files
- **Programming Language**: Python 3.11+
- **GUI Framework**: tkinter (standard library)
- **Test Coverage**: 100% of core algorithms
- **Game Mechanics**: Fully validated
- **User Experience**: Comprehensive feedback system

## 🎓 Learning Outcomes

### Technical Skills Demonstrated:
- [x] **Random Number Generation**: Secure random number generation
- [x] **Algorithm Design**: Optimal attempt calculation and hint generation
- [x] **GUI Development**: Advanced tkinter interface design
- [x] **Input Validation**: Comprehensive user input handling
- [x] **Game Logic**: Complex game state management
- [x] **Performance Analysis**: Mathematical performance evaluation
- [x] **Testing**: Automated testing and validation
- [x] **Documentation**: Professional project documentation

### Game Design Principles:
- [x] **User Experience**: Intuitive and engaging interface
- [x] **Difficulty Progression**: Balanced challenge levels
- [x] **Feedback Systems**: Clear, immediate feedback
- [x] **Hint Mechanics**: Helpful but not game-breaking
- [x] **Performance Incentives**: Encouraging optimal play

## 📝 Task Completion Summary

### ✅ **Requirements Met:**
- [x] Generates random number
- [x] Prompts user for guess input
- [x] Compares guess to generated number
- [x] Provides feedback (too high/too low)
- [x] Continues until correct guess
- [x] Displays number of attempts

### ✅ **Additional Features Implemented:**
- [x] Multiple difficulty levels
- [x] GUI and CLI versions
- [x] Hint system with multiple hint types
- [x] Performance rating system
- [x] Game statistics and history
- [x] Input validation and error handling
- [x] Automated testing suite
- [x] Professional documentation

### 🎯 **Key Innovations:**
- **Smart Attempt Limiting**: Uses mathematical optimization
- **Multi-Modal Hints**: Different hint strategies
- **Performance Analysis**: Compares to optimal play
- **Dual Interface**: Appeals to different user preferences
- **Comprehensive Testing**: Ensures reliability

## 👨‍💻 Author

**Created as part of the PRODIGY Software Development Internship Program**

- **Internship Program**: PRODIGY Software Development
- **Task**: Number Guessing Game
- **Completion Date**: July 2025
- **Technologies Used**: Python, tkinter, Random algorithms, Game design
- **Key Skills Demonstrated**: 
  - Game Development
  - Algorithm Design
  - GUI Development
  - Mathematical Optimization
  - Testing and Validation

---

**Task Status: ✅ COMPLETED SUCCESSFULLY**

**Ready to play? Let the guessing begin!** 🎯🎮
