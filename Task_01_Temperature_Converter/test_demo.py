"""
Test script for the Temperature Converter
This script demonstrates the core conversion functions
"""

def test_conversions():
    """Test the temperature conversion functions"""
    print("🧪 Testing Temperature Conversion Functions")
    print("=" * 50)
    
    # Test cases with known values
    test_cases = [
        # (value, from_unit, expected_celsius, expected_fahrenheit, expected_kelvin)
        (0, "celsius", 0, 32, 273.15),
        (100, "celsius", 100, 212, 373.15),
        (32, "fahrenheit", 0, 32, 273.15),
        (212, "fahrenheit", 100, 212, 373.15),
        (273.15, "kelvin", 0, 32, 273.15),
        (373.15, "kelvin", 100, 212, 373.15),
        (25, "celsius", 25, 77, 298.15),
        (-40, "celsius", -40, -40, 233.15),
    ]
    
    # Import conversion functions
    from temperature_converter_cli import TemperatureConverterCLI
    converter = TemperatureConverterCLI()
    
    passed = 0
    failed = 0
    
    for i, (value, from_unit, exp_c, exp_f, exp_k) in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {value}° {from_unit.title()}")
        
        # Get conversions
        results = converter.convert_all_units(value, from_unit)
        
        # Check results with tolerance for floating point precision
        tolerance = 0.01
        
        c_ok = abs(results['celsius'] - exp_c) < tolerance
        f_ok = abs(results['fahrenheit'] - exp_f) < tolerance
        k_ok = abs(results['kelvin'] - exp_k) < tolerance
        
        if c_ok and f_ok and k_ok:
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
            print(f"   Expected: C={exp_c}, F={exp_f}, K={exp_k}")
            print(f"   Got:      C={results['celsius']:.2f}, F={results['fahrenheit']:.2f}, K={results['kelvin']:.2f}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print(f"✅ Success rate: {(passed/(passed+failed)*100):.1f}%")
    
    return failed == 0

def demo_gui():
    """Demo the GUI version"""
    print("\n🖥️ Starting GUI Demo...")
    print("💡 The GUI window will open shortly.")
    print("💡 Try entering different temperature values!")
    
    try:
        import temperature_converter
        temperature_converter.main()
    except ImportError as e:
        print(f"❌ Could not import GUI version: {e}")
    except Exception as e:
        print(f"❌ Error running GUI: {e}")

def demo_cli():
    """Demo the CLI version"""
    print("\n💻 Starting CLI Demo...")
    print("💡 This will demonstrate the command-line interface.")
    
    try:
        import temperature_converter_cli
        temperature_converter_cli.main()
    except ImportError as e:
        print(f"❌ Could not import CLI version: {e}")
    except Exception as e:
        print(f"❌ Error running CLI: {e}")

def main():
    """Main function to run tests and demos"""
    print("🌡️ Temperature Converter - Test & Demo Script")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Run conversion tests")
        print("2. Demo GUI version")
        print("3. Demo CLI version")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            test_conversions()
        elif choice == '2':
            demo_gui()
        elif choice == '3':
            demo_cli()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
