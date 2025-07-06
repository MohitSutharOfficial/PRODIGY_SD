"""
Test and Demo Script for the Number Guessing Game
This script demonstrates and tests the core game functions
"""

import random
import time

def test_number_generation():
    """Test random number generation within different ranges"""
    print("🧪 Testing Random Number Generation")
    print("=" * 50)
    
    test_ranges = [
        (1, 10),
        (1, 50),
        (1, 100),
        (50, 150),
        (1, 500)
    ]
    
    passed = 0
    total = len(test_ranges)
    
    for min_val, max_val in test_ranges:
        print(f"\n🔍 Testing range {min_val}-{max_val}:")
        
        # Generate 10 random numbers and check if they're in range
        valid_numbers = 0
        for _ in range(10):
            num = random.randint(min_val, max_val)
            if min_val <= num <= max_val:
                valid_numbers += 1
        
        if valid_numbers == 10:
            print(f"✅ PASSED - All numbers in range {min_val}-{max_val}")
            passed += 1
        else:
            print(f"❌ FAILED - {valid_numbers}/10 numbers in range")
    
    print(f"\n📊 Random Generation Test Results: {passed}/{total} passed")
    return passed == total

def test_guess_validation():
    """Test guess validation logic"""
    print("\n🧪 Testing Guess Validation Logic")
    print("=" * 50)
    
    test_cases = [
        # (guess, secret, min_range, max_range, expected_result)
        (50, 50, 1, 100, "correct"),
        (25, 50, 1, 100, "too_low"),
        (75, 50, 1, 100, "too_high"),
        (0, 50, 1, 100, "out_of_range"),
        (101, 50, 1, 100, "out_of_range"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for guess, secret, min_range, max_range, expected in test_cases:
        print(f"\n🔍 Testing: guess={guess}, secret={secret}, range={min_range}-{max_range}")
        
        # Validate guess
        if guess < min_range or guess > max_range:
            result = "out_of_range"
        elif guess == secret:
            result = "correct"
        elif guess < secret:
            result = "too_low"
        else:
            result = "too_high"
        
        if result == expected:
            print(f"✅ PASSED - Expected: {expected}, Got: {result}")
            passed += 1
        else:
            print(f"❌ FAILED - Expected: {expected}, Got: {result}")
    
    print(f"\n📊 Validation Test Results: {passed}/{total} passed")
    return passed == total

def test_performance_rating():
    """Test performance rating calculation"""
    print("\n🧪 Testing Performance Rating System")
    print("=" * 50)
    
    def get_performance_rating(attempts, min_range, max_range):
        """Calculate performance rating based on attempts"""
        optimal_attempts = max(1, int((max_range - min_range + 1).bit_length()) - 1)
        
        if attempts <= optimal_attempts:
            return "🏆 Excellent!"
        elif attempts <= optimal_attempts + 2:
            return "🥇 Great!"
        elif attempts <= optimal_attempts + 4:
            return "🥈 Good!"
        else:
            return "🥉 Fair"
    
    test_cases = [
        # (attempts, min_range, max_range, expected_category)
        (1, 1, 100, "Excellent"),
        (3, 1, 100, "Excellent"),
        (6, 1, 100, "Excellent"),
        (8, 1, 100, "Great"),
        (10, 1, 100, "Good"),
        (12, 1, 100, "Fair"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for attempts, min_range, max_range, expected_category in test_cases:
        rating = get_performance_rating(attempts, min_range, max_range)
        result_category = rating.split()[1].replace("!", "")
        
        print(f"🔍 {attempts} attempts in range {min_range}-{max_range}: {rating}")
        
        if expected_category in rating:
            print(f"✅ PASSED")
            passed += 1
        else:
            print(f"❌ FAILED - Expected category: {expected_category}")
    
    print(f"\n📊 Performance Rating Test Results: {passed}/{total} passed")
    return passed == total

def demo_game_simulation():
    """Demonstrate a simulated game"""
    print("\n🎮 Game Simulation Demo")
    print("=" * 50)
    
    # Simulate a game
    min_range, max_range = 1, 100
    secret_number = random.randint(min_range, max_range)
    attempts = 0
    max_attempts = 10
    
    print(f"🎯 Secret number: {secret_number} (for demo purposes)")
    print(f"🔢 Range: {min_range} - {max_range}")
    print(f"🎮 Max attempts: {max_attempts}")
    print("-" * 50)
    
    # Simulate smart guessing strategy (binary search)
    low, high = min_range, max_range
    
    while attempts < max_attempts:
        attempts += 1
        guess = (low + high) // 2
        
        print(f"🤔 Attempt {attempts}: Guessing {guess}")
        
        if guess == secret_number:
            print(f"🎉 Correct! Found {secret_number} in {attempts} attempts!")
            break
        elif guess < secret_number:
            print(f"📈 Too low! Adjusting range to {guess + 1}-{high}")
            low = guess + 1
        else:
            print(f"📉 Too high! Adjusting range to {low}-{guess - 1}")
            high = guess - 1
        
        time.sleep(0.5)  # Small delay for readability
    
    if attempts >= max_attempts and guess != secret_number:
        print(f"😞 Game over! The number was {secret_number}")
    
    print(f"\n📊 Demo completed in {attempts} attempts")

def demo_gui():
    """Demo the GUI version"""
    print("\n🖥️ Starting GUI Demo...")
    print("💡 The GUI window will open shortly.")
    print("💡 Try different difficulty levels and features!")
    
    try:
        import guessing_game
        guessing_game.main()
    except ImportError as e:
        print(f"❌ Could not import GUI version: {e}")
    except Exception as e:
        print(f"❌ Error running GUI: {e}")

def demo_cli():
    """Demo the CLI version"""
    print("\n💻 Starting CLI Demo...")
    print("💡 This will start the command-line version.")
    
    try:
        import guessing_game_cli
        guessing_game_cli.main()
    except ImportError as e:
        print(f"❌ Could not import CLI version: {e}")
    except Exception as e:
        print(f"❌ Error running CLI: {e}")

def run_all_tests():
    """Run all test functions"""
    print("🧪 Running All Tests for Number Guessing Game")
    print("=" * 60)
    
    test_results = []
    
    # Run tests
    test_results.append(("Random Number Generation", test_number_generation()))
    test_results.append(("Guess Validation", test_guess_validation()))
    test_results.append(("Performance Rating", test_performance_rating()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    success_rate = (passed / total) * 100
    print(f"✅ Success Rate: {success_rate:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! The game is ready to play!")
    else:
        print("\n⚠️  Some tests failed. Please review the implementation.")

def main():
    """Main function to run tests and demos"""
    print("🎯 Number Guessing Game - Test & Demo Script")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Run all tests")
        print("2. Demo game simulation")
        print("3. Demo GUI version")
        print("4. Demo CLI version")
        print("5. Test random number generation")
        print("6. Test guess validation")
        print("7. Test performance rating")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            run_all_tests()
        elif choice == '2':
            demo_game_simulation()
        elif choice == '3':
            demo_gui()
        elif choice == '4':
            demo_cli()
        elif choice == '5':
            test_number_generation()
        elif choice == '6':
            test_guess_validation()
        elif choice == '7':
            test_performance_rating()
        elif choice == '8':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()
