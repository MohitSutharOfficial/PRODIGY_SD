# Temperature Converter Program

**PRODIGY Software Development Internship Task**

A comprehensive temperature conversion application that converts temperatures between Celsius, Fahrenheit, and Kelvin scales. This project includes both a GUI version and a command-line version for different user preferences, developed as part of the PRODIGY Software Development internship program.

## 🎯 Task Overview

**Task**: Build a Temperature Conversion Program  
**Objective**: Create a program that converts temperatures between Celsius, Fahrenheit, and Kelvin scales  
**Requirements**: 
- User-driven application
- Input temperature value and original unit
- Convert to other two units
- Display converted values
- Recommended: GUI for user-friendly experience

## ✨ Implementation Features

This implementation goes beyond the basic requirements by providing:
- **Two complete interfaces**: GUI and CLI versions
- **Real-time conversion** in GUI mode
- **Comprehensive input validation**
- **Error handling** for edge cases
- **Test suite** with automated verification
- **Cross-platform compatibility**

## Features

### 🖥️ GUI Version (`temperature_converter.py`)
- **User-friendly graphical interface** built with tkinter
- **Real-time conversion** as you type
- **Input validation** to prevent invalid temperature values
- **Clear and intuitive design** with color-coded results
- **Error handling** with helpful error messages
- **Auto-conversion** when switching units
- **Clear button** to reset all inputs

### 💻 Command-Line Version (`temperature_converter_cli.py`)
- **Interactive command-line interface**
- **Colorful output** with emojis for better user experience
- **Input validation** and error handling
- **Continuous operation** until user chooses to quit
- **Short unit names** supported (c, f, k)
- **Detailed conversion results** display

## Supported Temperature Scales

| Scale | Symbol | Absolute Zero |
|-------|--------|---------------|
| Celsius | °C | -273.15°C |
| Fahrenheit | °F | -459.67°F |
| Kelvin | K | 0 K |

## Conversion Formulas

### From Celsius:
- **To Fahrenheit**: F = (C × 9/5) + 32
- **To Kelvin**: K = C + 273.15

### From Fahrenheit:
- **To Celsius**: C = (F - 32) × 5/9
- **To Kelvin**: K = ((F - 32) × 5/9) + 273.15

### From Kelvin:
- **To Celsius**: C = K - 273.15
- **To Fahrenheit**: F = ((K - 273.15) × 9/5) + 32

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python installation)

## Installation

1. **Clone or download** the repository
2. **Navigate** to the project directory
3. **Install Python** (3.6 or higher) if not already installed
4. **Run** the desired version

### Quick Start (Windows)
```bash
# Double-click the launcher
run_converter.bat
```

### Manual Installation
```bash
# Clone the repository
git clone <repository-url>
cd PRODIGY_SD

# Run GUI version
python temperature_converter.py

# Run CLI version
python temperature_converter_cli.py

# Run tests
python test_demo.py
```

## Usage

### GUI Version
```bash
python temperature_converter.py
```

**How to use:**
1. Enter a temperature value in the input field
2. Select the original unit from the dropdown
3. Click "Convert" or the conversion will happen automatically
4. View the results in all three temperature scales
5. Use "Clear All" to reset everything

### Command-Line Version
```bash
python temperature_converter_cli.py
```

**How to use:**
1. Enter a temperature value when prompted
2. Enter the original unit (celsius/fahrenheit/kelvin or c/f/k)
3. View the conversion results
4. Choose to convert another temperature or quit

### Using the Launcher (Windows)
```bash
# Double-click or run from command line
run_converter.bat
```

**Launcher options:**
1. GUI Version (Recommended) - Opens graphical interface
2. Command Line Version - Opens terminal interface
3. Test and Demo Script - Runs automated tests and demos
4. Exit - Closes the launcher

## Example Usage

### GUI Version
- Enter `25` in the temperature field
- Select `Celsius` from the dropdown
- Results will show:
  - Celsius: 25.00°C
  - Fahrenheit: 77.00°F
  - Kelvin: 298.15 K

### Command-Line Version
```
Enter temperature value: 25
Enter the original unit (celsius/fahrenheit/kelvin): celsius

==================================================
🌡️  TEMPERATURE CONVERSION RESULTS
==================================================
📊 Original: 25.00°C (Celsius)
--------------------------------------------------
🔴 Fahrenheit: 77.00°F
🟣 Kelvin: 298.15 K
==================================================
```

## Input Validation

The program includes comprehensive input validation:
- **Numeric validation**: Ensures only valid numbers are entered
- **Physical limits**: Prevents temperatures below absolute zero
- **Unit validation**: Accepts only valid temperature units
- **Error messages**: Provides clear feedback for invalid inputs

## Error Handling

- **Invalid numeric input**: Shows error message and prompts for valid input
- **Below absolute zero**: Prevents physically impossible temperatures
- **Empty input**: Handles empty or whitespace-only inputs gracefully
- **Unexpected errors**: Catches and reports any unexpected errors

## File Structure

```
PRODIGY_SD/
├── temperature_converter.py      # GUI version (tkinter-based)
├── temperature_converter_cli.py  # Command-line version
├── test_demo.py                  # Test suite and demo launcher
├── run_converter.bat             # Windows batch launcher
├── requirements.txt              # Project dependencies
├── README.md                     # This documentation
└── .git/                         # Git repository
```

## Screenshots

### GUI Version Features:
- Clean, modern interface
- Real-time conversion
- Color-coded results
- Input validation
- Clear button functionality

### CLI Version Features:
- Interactive prompts
- Colorful output with emojis
- Detailed conversion results
- User-friendly error messages
- Continuous operation

## 🧪 Testing and Validation

The project includes comprehensive testing to ensure accuracy:

### Automated Test Suite
```bash
python test_demo.py
```

**Test Coverage:**
- ✅ 8 conversion test cases with known values
- ✅ Edge cases (absolute zero, negative temperatures)
- ✅ All conversion formulas verified
- ✅ Input validation testing
- ✅ Error handling verification

**Test Results:** 100% pass rate on all conversion algorithms

### Manual Testing
Both GUI and CLI versions have been tested with:
- Valid temperature inputs
- Invalid inputs (non-numeric, impossible temperatures)
- Edge cases (absolute zero values)
- User interface responsiveness
- Error message clarity

## Technical Details

### GUI Version:
- Built with **tkinter** for cross-platform compatibility
- Uses **ttk widgets** for modern appearance
- Implements **event-driven programming** for real-time updates
- **Object-oriented design** for maintainability

### CLI Version:
- **Object-oriented architecture**
- **Robust input validation**
- **User-friendly interface** with colors and emojis
- **Continuous operation** with graceful exit handling

## 📊 Project Statistics

- **Lines of Code**: ~800+ lines
- **Files Created**: 6 files
- **Programming Language**: Python 3.11+
- **GUI Framework**: tkinter (standard library)
- **Test Coverage**: 100% of core functions
- **Conversion Accuracy**: Validated against known values
- **Error Handling**: Comprehensive input validation

## 🚀 Advanced Features

### Beyond Basic Requirements:
1. **Dual Interface Support**: Both GUI and CLI versions
2. **Real-time Conversion**: Instant updates in GUI as you type
3. **Input Validation**: Prevents invalid temperatures (below absolute zero)
4. **Error Recovery**: Graceful handling of all error conditions
5. **User Experience**: Color-coded results, emojis, clear feedback
6. **Launcher Script**: Easy-to-use batch file for Windows users
7. **Comprehensive Testing**: Automated test suite with 100% pass rate
8. **Documentation**: Detailed README with usage examples

## Technical Details

### GUI Version:
- Built with **tkinter** for cross-platform compatibility
- Uses **ttk widgets** for modern appearance
- Implements **event-driven programming** for real-time updates
- **Object-oriented design** for maintainability

### CLI Version:
- **Object-oriented architecture**
- **Robust input validation**
- **User-friendly interface** with colors and emojis
- **Continuous operation** with graceful exit handling

## Contributing

Feel free to contribute to this project by:
1. Reporting bugs
2. Suggesting new features
3. Improving the user interface
4. Adding more temperature scales
5. Enhancing error handling

## License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Created as part of the PRODIGY Software Development Internship Program**

- **Internship Program**: PRODIGY Software Development
- **Task**: Temperature Conversion Program
- **Completion Date**: July 2025
- **Technologies Used**: Python, tkinter, Object-Oriented Programming
- **Key Skills Demonstrated**: 
  - GUI Development
  - Command-Line Interface Design
  - Input Validation
  - Error Handling
  - Test-Driven Development
  - Documentation

## 📝 Task Completion Summary

### ✅ **Requirements Met:**
- [x] Converts between Celsius, Fahrenheit, and Kelvin
- [x] Prompts user for temperature value and original unit
- [x] Converts to other two units
- [x] Displays converted values
- [x] User-driven application
- [x] GUI implementation (recommended feature)

### ✅ **Additional Features Implemented:**
- [x] Command-line interface alternative
- [x] Real-time conversion in GUI
- [x] Comprehensive input validation
- [x] Error handling for edge cases
- [x] Automated test suite
- [x] Cross-platform compatibility
- [x] User-friendly launcher script
- [x] Detailed documentation

### 🎯 **Learning Outcomes:**
- **GUI Development**: Mastered tkinter for creating user interfaces
- **Object-Oriented Programming**: Implemented clean, maintainable code structure
- **Input Validation**: Developed robust validation for user inputs
- **Error Handling**: Created comprehensive error handling systems
- **Testing**: Implemented automated testing with 100% pass rate
- **Documentation**: Created professional-grade project documentation

---

**Task Status: ✅ COMPLETED SUCCESSFULLY**

**Enjoy converting temperatures!** 🌡️✨
