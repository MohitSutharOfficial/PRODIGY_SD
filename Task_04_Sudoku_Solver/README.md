# Sudoku Solver

A comprehensive Sudoku solving application with both GUI and CLI interfaces, featuring advanced backtracking algorithms, puzzle validation, and interactive solving capabilities.

## Features

### Core Functionality
- **Automatic Solving**: Advanced backtracking algorithm solves puzzles instantly
- **Puzzle Validation**: Comprehensive validation for puzzle correctness and conflicts
- **Multiple Input Methods**: Manual input, file import, and example puzzles
- **Animated Solving**: Step-by-step visualization of the solving process
- **Difficulty Assessment**: Automatic difficulty level detection
- **Complete Statistics**: Detailed puzzle analysis and metrics

### Advanced Features
- **Import/Export**: Load and save puzzles in JSON and text formats
- **Example Puzzles**: Pre-loaded puzzles of various difficulty levels
- **Interactive Interface**: Click-to-focus with related cell highlighting
- **Performance Metrics**: Detailed timing and performance analysis
- **Persistent Storage**: Save and load custom puzzle collections
- **Multiple Formats**: Support for various puzzle file formats

### User Interfaces
- **GUI Version**: Modern tkinter-based interface with visual feedback
- **CLI Version**: Command-line interface with rich text formatting
- **Animated Solver**: Real-time visualization of solving algorithm
- **Interactive Menus**: Intuitive navigation in both versions

## Files

- `sudoku_solver.py` - GUI version with tkinter interface
- `sudoku_solver_cli.py` - Command-line interface version
- `test_demo.py` - Comprehensive testing and demonstration script
- `run_sudoku.bat` - Windows batch launcher
- `requirements.txt` - Project dependencies (uses only standard library)
- `README.md` - This documentation file

## Installation

1. Ensure you have Python 3.6+ installed
2. No additional packages required - uses only Python standard library
3. Download all files to a folder
4. Run using the methods below

## Usage

### GUI Version (Recommended)
```bash
python sudoku_solver.py
```

### CLI Version
```bash
python sudoku_solver_cli.py
```

### Using the Batch Launcher (Windows)
```bash
run_sudoku.bat
```

### Running Tests and Demos
```bash
python test_demo.py
```

## GUI Interface Features

### Main Window
- **9x9 Grid**: Interactive Sudoku grid with 3x3 block separation
- **Visual Feedback**: Cell highlighting and color coding
- **Control Buttons**: Solve, Clear, Validate, and Example puzzles
- **Progress Bar**: Real-time solving progress visualization
- **Status Panel**: Detailed information and statistics

### Solving Features
- **Instant Solve**: Fast backtracking algorithm
- **Animated Solve**: Step-by-step visualization
- **Validation**: Check puzzle validity and conflicts
- **Statistics**: Real-time puzzle analysis

### File Operations
- **Load Puzzles**: Import from JSON or text files
- **Save Puzzles**: Export in multiple formats
- **Example Library**: Built-in puzzle collection
- **Custom Collections**: Save and organize puzzle sets

### Visual Elements
- **Color Coding**: Blue for original numbers, red for solutions
- **Cell Highlighting**: Related cells highlighted on focus
- **Progress Tracking**: Visual progress indicators
- **Error Detection**: Immediate conflict visualization

## CLI Interface Features

### Main Menu Options
1. **Input Puzzle**: Manual puzzle entry with multiple methods
2. **Solve Puzzle**: Instant solving with performance metrics
3. **Solve with Animation**: Step-by-step solving visualization
4. **Validate Puzzle**: Check puzzle correctness and solvability
5. **Show Statistics**: Detailed puzzle analysis
6. **Save Puzzle**: Store puzzles in custom collections
7. **Load Saved Puzzle**: Access previously saved puzzles
8. **Load Example**: Access built-in example puzzles
9. **Export Puzzle**: Save puzzles to files
10. **Import Puzzle**: Load puzzles from files
11. **Help**: Comprehensive help system
12. **Exit**: Save and exit application

### Input Methods
- **Row by Row**: Enter 9 numbers per row
- **Cell by Cell**: Specify individual cells (row, col, value)
- **File Import**: Load from JSON or text files
- **Example Selection**: Choose from pre-defined puzzles

### Advanced Features
- **Colored Output**: Visual distinction between original and solved numbers
- **Animation Control**: Step-by-step solving with pause capability
- **Performance Metrics**: Detailed timing and efficiency analysis
- **Batch Operations**: Process multiple puzzles efficiently

## Algorithm

### Backtracking Approach
1. **Find Empty Cell**: Locate next unfilled position
2. **Try Values**: Test numbers 1-9 in sequence
3. **Validate Placement**: Check row, column, and 3x3 box constraints
4. **Recursive Solve**: Continue with next empty cell
5. **Backtrack**: Remove invalid placements and try alternatives
6. **Solution Found**: Complete when all cells are filled

### Validation Rules
- **Row Constraint**: Each row must contain digits 1-9 exactly once
- **Column Constraint**: Each column must contain digits 1-9 exactly once
- **Box Constraint**: Each 3x3 box must contain digits 1-9 exactly once
- **Uniqueness**: Valid puzzles should have exactly one solution

### Performance Optimizations
- **Efficient Cell Selection**: Smart empty cell finding
- **Constraint Propagation**: Early conflict detection
- **Pruning**: Eliminate impossible branches quickly
- **Memory Management**: Minimal memory usage with deep copying

## Data Formats

### JSON Format
```json
{
  "grid": [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    ...
  ],
  "original_grid": [...],
  "difficulty": "Easy",
  "created": "2024-01-15T10:30:00",
  "statistics": {
    "filled": 30,
    "empty": 51,
    "completion": 37.0
  }
}
```

### Text Format
```
5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
8 . . . 6 . . . 3
4 . . 8 . 3 . . 1
7 . . . 2 . . . 6
. 6 . . . . 2 8 .
. . . 4 1 9 . . 5
. . . . 8 . . 7 9
```

## Difficulty Levels

### Classification System
- **Easy**: ≤40 empty cells (high number of clues)
- **Medium**: 41-50 empty cells (moderate clues)
- **Hard**: 51-60 empty cells (fewer clues)
- **Expert**: >60 empty cells (minimal clues)

### Characteristics
- **Easy Puzzles**: Quick solving, straightforward logic
- **Medium Puzzles**: Moderate complexity, some advanced techniques
- **Hard Puzzles**: Complex logic, multiple solution paths
- **Expert Puzzles**: Extreme difficulty, extensive backtracking

## Testing

The `test_demo.py` script includes comprehensive tests for:

### Unit Tests
- **Core Algorithm**: Backtracking solver validation
- **Validation Functions**: Constraint checking and conflict detection
- **Grid Operations**: Cell manipulation and state management
- **Performance**: Timing and efficiency measurements

### Integration Tests
- **File Operations**: Import/export functionality
- **Multiple Puzzles**: Various difficulty levels
- **GUI Components**: Interface element testing
- **CLI Operations**: Command-line functionality

### Performance Tests
- **Solving Speed**: Algorithm efficiency measurement
- **Memory Usage**: Resource consumption analysis
- **Large Datasets**: Bulk puzzle processing
- **Edge Cases**: Boundary condition testing

## Error Handling

### Robust Error Management
- **Invalid Input**: Comprehensive input validation
- **File Operations**: Graceful file handling errors
- **Algorithm Failures**: Unsolvable puzzle detection
- **Memory Issues**: Resource limitation handling

### User-Friendly Messages
- **Clear Error Reports**: Detailed error descriptions
- **Solution Suggestions**: Helpful troubleshooting guidance
- **Recovery Options**: Graceful failure recovery
- **Debug Information**: Developer-friendly diagnostics

## Performance

### Optimization Features
- **Fast Algorithm**: Efficient backtracking implementation
- **Memory Efficient**: Minimal memory footprint
- **Responsive UI**: Non-blocking interface operations
- **Batch Processing**: Multiple puzzle handling

### Benchmarks
- **Easy Puzzles**: Typical solving time <0.01 seconds
- **Medium Puzzles**: Typical solving time <0.1 seconds
- **Hard Puzzles**: Typical solving time <1.0 seconds
- **Expert Puzzles**: Typical solving time <10.0 seconds

## Development

### Code Structure
- **SudokuSolver Class**: Core algorithm implementation
- **SudokuGUI Class**: Tkinter interface components
- **SudokuCLI Class**: Command-line interface handlers
- **Utility Functions**: Helper functions and validation

### Best Practices
- **Clean Code**: Well-structured, documented implementation
- **Object-Oriented**: Modular design with clear separation
- **Error Handling**: Comprehensive exception management
- **Testing**: Extensive test coverage and validation

## Compatibility

- **Python Version**: 3.6+
- **Operating System**: Windows, macOS, Linux
- **GUI Framework**: tkinter (included with Python)
- **Dependencies**: Python standard library only

## Future Enhancements

### Planned Features
- **Puzzle Generation**: Create new puzzles algorithmically
- **Hint System**: Provide solving hints and suggestions
- **Multiple Solving Strategies**: Advanced solving techniques
- **Puzzle Rating**: Sophisticated difficulty assessment
- **Tournament Mode**: Competitive solving features

### Technical Improvements
- **Advanced Algorithms**: Constraint satisfaction techniques
- **Performance Optimization**: Further speed improvements
- **Enhanced UI**: More sophisticated interface elements
- **Database Integration**: Persistent puzzle storage
- **Web Interface**: Browser-based version

## Educational Value

### Learning Outcomes
- **Algorithm Design**: Backtracking and recursion concepts
- **Problem Solving**: Systematic approach to complex problems
- **Data Structures**: Grid manipulation and state management
- **User Interface**: GUI and CLI development principles
- **Testing**: Comprehensive validation and verification

### Programming Concepts
- **Recursion**: Deep recursive problem solving
- **Backtracking**: Systematic search with pruning
- **Validation**: Constraint checking and verification
- **File I/O**: Data persistence and format handling
- **Object-Oriented Programming**: Clean code organization

## License

This project is part of the PRODIGY InfoTech internship program and is intended for educational purposes.

## Support

For questions, issues, or suggestions, please refer to the main project documentation or contact the development team.

---

**Sudoku Solver** - Bringing the power of algorithmic problem-solving to classic puzzles! 🧩✨
