"""
Test and Demo Script for the Sudoku Solver
This script demonstrates and tests the core Sudoku solving functions
"""

import copy
import time
import json
import tempfile
import os
from datetime import datetime

def test_sudoku_solver():
    """Test the core Sudoku solving functionality"""
    print("🧪 Testing Sudoku Solver Core Functions")
    print("=" * 50)
    
    # Import the solver
    from sudoku_solver_cli import SudokuSolver
    
    # Test puzzle (easy)
    test_puzzle = [
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
    
    expected_solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    
    solver = SudokuSolver()
    solver.grid = copy.deepcopy(test_puzzle)
    solver.original_grid = copy.deepcopy(test_puzzle)
    
    print("🔍 Testing puzzle solving...")
    start_time = time.time()
    success = solver.solve_sudoku()
    solve_time = time.time() - start_time
    
    if success:
        print("✅ PASSED - Puzzle solved successfully")
        print(f"   Solve time: {solve_time:.4f} seconds")
        
        # Verify solution
        if solver.grid == expected_solution:
            print("✅ PASSED - Solution is correct")
        else:
            print("❌ FAILED - Solution is incorrect")
            return False
    else:
        print("❌ FAILED - Could not solve puzzle")
        return False
    
    print("\n🔍 Testing validation functions...")
    
    # Test valid puzzle
    if solver.is_valid_puzzle(test_puzzle):
        print("✅ PASSED - Valid puzzle recognized")
    else:
        print("❌ FAILED - Valid puzzle not recognized")
        return False
    
    # Test invalid puzzle
    invalid_puzzle = copy.deepcopy(test_puzzle)
    invalid_puzzle[0][0] = 6  # Create conflict with existing 6 in row
    if not solver.is_valid_puzzle(invalid_puzzle):
        print("✅ PASSED - Invalid puzzle detected")
    else:
        print("❌ FAILED - Invalid puzzle not detected")
        return False
    
    print("\n🔍 Testing difficulty assessment...")
    difficulty = solver.get_difficulty_level(test_puzzle)
    print(f"   Difficulty: {difficulty}")
    
    if difficulty in ["Easy", "Medium", "Hard", "Expert"]:
        print("✅ PASSED - Difficulty assessment working")
    else:
        print("❌ FAILED - Difficulty assessment error")
        return False
    
    print("\n🔍 Testing statistics...")
    stats = solver.get_statistics(test_puzzle)
    expected_filled = 30  # Count of non-zero cells in test puzzle
    
    if stats['filled'] == expected_filled:
        print("✅ PASSED - Statistics calculation correct")
    else:
        print(f"❌ FAILED - Expected {expected_filled} filled cells, got {stats['filled']}")
        return False
    
    return True

def test_validation_functions():
    """Test validation and helper functions"""
    print("\n🧪 Testing Validation Functions")
    print("=" * 40)
    
    from sudoku_solver_cli import SudokuSolver
    
    solver = SudokuSolver()
    
    # Test empty grid
    empty_grid = [[0 for _ in range(9)] for _ in range(9)]
    
    print("🔍 Testing empty grid validation...")
    if solver.is_valid_puzzle(empty_grid):
        print("✅ PASSED - Empty grid is valid")
    else:
        print("❌ FAILED - Empty grid should be valid")
        return False
    
    # Test individual cell validation
    print("\n🔍 Testing cell validation...")
    test_grid = [[0 for _ in range(9)] for _ in range(9)]
    test_grid[0][0] = 5
    
    # Should be invalid to place 5 in same row
    if not solver.is_valid(test_grid, 0, 1, 5):
        print("✅ PASSED - Row conflict detected")
    else:
        print("❌ FAILED - Row conflict not detected")
        return False
    
    # Should be invalid to place 5 in same column
    if not solver.is_valid(test_grid, 1, 0, 5):
        print("✅ PASSED - Column conflict detected")
    else:
        print("❌ FAILED - Column conflict not detected")
        return False
    
    # Should be invalid to place 5 in same 3x3 box
    if not solver.is_valid(test_grid, 1, 1, 5):
        print("✅ PASSED - Box conflict detected")
    else:
        print("❌ FAILED - Box conflict not detected")
        return False
    
    # Should be valid to place 5 in different box
    if solver.is_valid(test_grid, 3, 3, 5):
        print("✅ PASSED - Valid placement recognized")
    else:
        print("❌ FAILED - Valid placement not recognized")
        return False
    
    return True

def test_multiple_puzzles():
    """Test solver with multiple puzzle difficulties"""
    print("\n🧪 Testing Multiple Puzzle Difficulties")
    print("=" * 45)
    
    from sudoku_solver_cli import SudokuSolver
    
    puzzles = {
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
    
    solver = SudokuSolver()
    passed = 0
    total = len(puzzles)
    
    for difficulty, puzzle in puzzles.items():
        print(f"\n🔍 Testing {difficulty} puzzle...")
        
        solver.grid = copy.deepcopy(puzzle)
        solver.original_grid = copy.deepcopy(puzzle)
        
        start_time = time.time()
        success = solver.solve_sudoku()
        solve_time = time.time() - start_time
        
        if success:
            print(f"✅ PASSED - {difficulty} puzzle solved in {solve_time:.4f}s")
            passed += 1
            
            # Verify solution is complete
            if all(all(cell != 0 for cell in row) for row in solver.grid):
                print(f"✅ PASSED - {difficulty} solution is complete")
            else:
                print(f"❌ FAILED - {difficulty} solution incomplete")
                passed -= 1
        else:
            print(f"❌ FAILED - {difficulty} puzzle could not be solved")
    
    print(f"\n📊 Multiple Puzzle Test Results: {passed}/{total} passed")
    return passed == total

def test_file_operations():
    """Test file import/export functionality"""
    print("\n🧪 Testing File Operations")
    print("=" * 35)
    
    from sudoku_solver_cli import SudokuSolver
    
    solver = SudokuSolver()
    
    # Test puzzle
    test_puzzle = [
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
    
    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        json_file = os.path.join(temp_dir, "test_puzzle.json")
        txt_file = os.path.join(temp_dir, "test_puzzle.txt")
        
        print("🔍 Testing JSON export/import...")
        
        # Test JSON export
        try:
            data = {
                'grid': test_puzzle,
                'original_grid': test_puzzle,
                'exported': datetime.now().isoformat(),
                'statistics': solver.get_statistics(test_puzzle)
            }
            
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print("✅ PASSED - JSON export successful")
        except Exception as e:
            print(f"❌ FAILED - JSON export error: {e}")
            return False
        
        # Test JSON import
        try:
            with open(json_file, 'r') as f:
                imported_data = json.load(f)
            
            if imported_data['grid'] == test_puzzle:
                print("✅ PASSED - JSON import successful")
            else:
                print("❌ FAILED - JSON import data mismatch")
                return False
        except Exception as e:
            print(f"❌ FAILED - JSON import error: {e}")
            return False
        
        print("\n🔍 Testing text file export/import...")
        
        # Test text export
        try:
            with open(txt_file, 'w') as f:
                f.write("Sudoku Puzzle\n")
                f.write("=" * 15 + "\n\n")
                for row in test_puzzle:
                    f.write(' '.join(str(cell) if cell != 0 else '.' for cell in row) + '\n')
            
            print("✅ PASSED - Text export successful")
        except Exception as e:
            print(f"❌ FAILED - Text export error: {e}")
            return False
        
        # Test text import
        try:
            with open(txt_file, 'r') as f:
                lines = f.readlines()
                
            imported_grid = []
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
                        imported_grid.append(row)
                    if len(imported_grid) == 9:
                        break
            
            if imported_grid == test_puzzle:
                print("✅ PASSED - Text import successful")
            else:
                print("❌ FAILED - Text import data mismatch")
                return False
        except Exception as e:
            print(f"❌ FAILED - Text import error: {e}")
            return False
    
    return True

def test_performance():
    """Test solver performance with various puzzles"""
    print("\n🧪 Testing Performance")
    print("=" * 30)
    
    from sudoku_solver_cli import SudokuSolver
    
    # Different complexity puzzles
    puzzles = {
        "Quick Solve": [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 0]  # Only one empty cell
        ],
        "Medium Solve": [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ]
    }
    
    solver = SudokuSolver()
    
    for name, puzzle in puzzles.items():
        print(f"\n🔍 Testing {name}...")
        
        solver.grid = copy.deepcopy(puzzle)
        start_time = time.time()
        success = solver.solve_sudoku()
        solve_time = time.time() - start_time
        
        if success:
            print(f"✅ PASSED - {name} solved in {solve_time:.4f} seconds")
            
            # Performance benchmarks
            if solve_time < 0.1:
                print("🚀 EXCELLENT - Very fast solution")
            elif solve_time < 1.0:
                print("⚡ GOOD - Fast solution")
            elif solve_time < 5.0:
                print("⏱️  ACCEPTABLE - Reasonable solution time")
            else:
                print("⚠️  SLOW - Solution took longer than expected")
        else:
            print(f"❌ FAILED - {name} could not be solved")
            return False
    
    return True

def demo_gui():
    """Demo the GUI version"""
    print("\n🖥️ Starting GUI Demo...")
    print("💡 The GUI window will open shortly.")
    print("💡 Try the following features:")
    print("   • Solve the sample puzzle")
    print("   • Load example puzzles")
    print("   • Use the animated solver")
    print("   • Validate puzzles")
    print("   • Save/load puzzles")
    print("   • Input your own puzzle")
    print("\nClose the GUI window to return to the demo menu.")
    
    try:
        from sudoku_solver import SudokuGUI
        app = SudokuGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return False
    
    return True

def demo_cli():
    """Demo the CLI version"""
    print("\n💻 Starting CLI Demo...")
    print("💡 This will start the command-line interface.")
    print("💡 Try the following features:")
    print("   • Load example puzzles")
    print("   • Solve puzzles")
    print("   • Use animated solving")
    print("   • Input your own puzzle")
    print("   • Save/load puzzles")
    print("   • Validate puzzles")
    print("\nChoose option 12 to exit and return to the demo menu.")
    
    try:
        from sudoku_solver_cli import SudokuCLI
        app = SudokuCLI()
        app.run()
    except Exception as e:
        print(f"❌ Error starting CLI: {e}")
        return False
    
    return True

def create_sample_puzzles():
    """Create sample puzzle files for testing"""
    print("\n📝 Creating Sample Puzzle Files")
    print("=" * 40)
    
    sample_puzzles = {
        "easy_puzzle": {
            "name": "Easy Sample",
            "grid": [
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
        },
        "medium_puzzle": {
            "name": "Medium Sample",
            "grid": [
                [0, 0, 0, 6, 0, 0, 4, 0, 0],
                [7, 0, 0, 0, 0, 3, 6, 0, 0],
                [0, 0, 0, 0, 9, 1, 0, 8, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 0, 1, 8, 0, 0, 0, 3],
                [0, 0, 0, 3, 0, 6, 0, 4, 5],
                [0, 4, 0, 2, 0, 0, 0, 6, 0],
                [9, 0, 3, 0, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 1, 0, 0]
            ]
        },
        "hard_puzzle": {
            "name": "Hard Sample",
            "grid": [
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
    }
    
    created_files = []
    
    for filename, puzzle_data in sample_puzzles.items():
        # Create JSON file
        json_filename = f"{filename}.json"
        try:
            data = {
                'grid': puzzle_data['grid'],
                'original_grid': puzzle_data['grid'],
                'name': puzzle_data['name'],
                'created': datetime.now().isoformat(),
                'difficulty': 'Unknown'
            }
            
            with open(json_filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Created {json_filename}")
            created_files.append(json_filename)
        except Exception as e:
            print(f"❌ Error creating {json_filename}: {e}")
        
        # Create text file
        txt_filename = f"{filename}.txt"
        try:
            with open(txt_filename, 'w') as f:
                f.write(f"Sudoku Puzzle: {puzzle_data['name']}\n")
                f.write("=" * 30 + "\n\n")
                for row in puzzle_data['grid']:
                    f.write(' '.join(str(cell) if cell != 0 else '.' for cell in row) + '\n')
            
            print(f"✅ Created {txt_filename}")
            created_files.append(txt_filename)
        except Exception as e:
            print(f"❌ Error creating {txt_filename}: {e}")
    
    print(f"\n💾 Created {len(created_files)} sample files")
    print("💡 You can import these files in the main application")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("🧪 Running All Tests for Sudoku Solver")
    print("=" * 50)
    
    tests = [
        ("Core Solver Functions", test_sudoku_solver),
        ("Validation Functions", test_validation_functions),
        ("Multiple Puzzles", test_multiple_puzzles),
        ("File Operations", test_file_operations),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} tests failed")
        except Exception as e:
            print(f"❌ {test_name} tests error: {e}")
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    for i, (test_name, _) in enumerate(tests):
        if i < passed:
            print(f"✅ {test_name}")
        else:
            print(f"❌ {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    print(f"✅ Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! The Sudoku solver is ready!")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

def main():
    """Main demo function"""
    print("🧩 Sudoku Solver - Test & Demo Script")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Run all tests")
        print("2. Test core functions")
        print("3. Test validation functions")
        print("4. Test multiple puzzles")
        print("5. Test file operations")
        print("6. Test performance")
        print("7. Demo GUI version")
        print("8. Demo CLI version")
        print("9. Create sample files")
        print("10. Exit")
        
        try:
            choice = input("\nEnter your choice (1-10): ").strip()
            
            if choice == '1':
                run_all_tests()
                # For automated testing, exit after running all tests
                import sys
                if not sys.stdin.isatty():
                    print("👋 Automated testing complete!")
                    break
            elif choice == '2':
                test_sudoku_solver()
            elif choice == '3':
                test_validation_functions()
            elif choice == '4':
                test_multiple_puzzles()
            elif choice == '5':
                test_file_operations()
            elif choice == '6':
                test_performance()
            elif choice == '7':
                demo_gui()
            elif choice == '8':
                demo_cli()
            elif choice == '9':
                create_sample_puzzles()
            elif choice == '10':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-10.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Input stream ended. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
