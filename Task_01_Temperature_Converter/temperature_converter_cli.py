"""
Temperature Converter - Command Line Version
A simple command-line program to convert temperatures between Celsius, Fahrenheit, and Kelvin.
"""

class TemperatureConverterCLI:
    def __init__(self):
        self.conversions = {
            'celsius': {
                'fahrenheit': self.celsius_to_fahrenheit,
                'kelvin': self.celsius_to_kelvin
            },
            'fahrenheit': {
                'celsius': self.fahrenheit_to_celsius,
                'kelvin': self.fahrenheit_to_kelvin
            },
            'kelvin': {
                'celsius': self.kelvin_to_celsius,
                'fahrenheit': self.kelvin_to_fahrenheit
            }
        }
    
    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
    def celsius_to_kelvin(self, celsius):
        """Convert Celsius to Kelvin"""
        return celsius + 273.15
    
    def fahrenheit_to_celsius(self, fahrenheit):
        """Convert Fahrenheit to Celsius"""
        return (fahrenheit - 32) * 5/9
    
    def fahrenheit_to_kelvin(self, fahrenheit):
        """Convert Fahrenheit to Kelvin"""
        celsius = self.fahrenheit_to_celsius(fahrenheit)
        return self.celsius_to_kelvin(celsius)
    
    def kelvin_to_celsius(self, kelvin):
        """Convert Kelvin to Celsius"""
        return kelvin - 273.15
    
    def kelvin_to_fahrenheit(self, kelvin):
        """Convert Kelvin to Fahrenheit"""
        celsius = self.kelvin_to_celsius(kelvin)
        return self.celsius_to_fahrenheit(celsius)
    
    def validate_temperature(self, value, unit):
        """Validate temperature input based on unit"""
        if unit.lower() == "kelvin" and value < 0:
            return False, "Kelvin temperature cannot be negative (absolute zero is 0 K)"
        elif unit.lower() == "celsius" and value < -273.15:
            return False, "Celsius temperature cannot be below -273.15°C (absolute zero)"
        elif unit.lower() == "fahrenheit" and value < -459.67:
            return False, "Fahrenheit temperature cannot be below -459.67°F (absolute zero)"
        return True, ""
    
    def get_temperature_input(self):
        """Get temperature value from user"""
        while True:
            try:
                temp_str = input("Enter temperature value: ").strip()
                if temp_str.lower() == 'quit':
                    return None
                temp_value = float(temp_str)
                return temp_value
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
                print("💡 Type 'quit' to exit the program.")
    
    def get_unit_input(self, prompt):
        """Get unit selection from user"""
        valid_units = ['celsius', 'fahrenheit', 'kelvin', 'c', 'f', 'k']
        unit_mapping = {
            'c': 'celsius',
            'f': 'fahrenheit',
            'k': 'kelvin'
        }
        
        while True:
            unit = input(prompt).strip().lower()
            if unit == 'quit':
                return None
            
            if unit in unit_mapping:
                unit = unit_mapping[unit]
            
            if unit in valid_units:
                return unit
            else:
                print("❌ Invalid unit! Please enter 'celsius', 'fahrenheit', 'kelvin' (or 'c', 'f', 'k').")
                print("💡 Type 'quit' to exit the program.")
    
    def convert_all_units(self, temp_value, from_unit):
        """Convert temperature to all other units"""
        results = {}
        
        if from_unit == 'celsius':
            results['celsius'] = temp_value
            results['fahrenheit'] = self.celsius_to_fahrenheit(temp_value)
            results['kelvin'] = self.celsius_to_kelvin(temp_value)
        elif from_unit == 'fahrenheit':
            results['fahrenheit'] = temp_value
            results['celsius'] = self.fahrenheit_to_celsius(temp_value)
            results['kelvin'] = self.fahrenheit_to_kelvin(temp_value)
        else:  # kelvin
            results['kelvin'] = temp_value
            results['celsius'] = self.kelvin_to_celsius(temp_value)
            results['fahrenheit'] = self.kelvin_to_fahrenheit(temp_value)
        
        return results
    
    def display_results(self, results, original_unit, original_value):
        """Display conversion results"""
        print("\n" + "="*50)
        print("🌡️  TEMPERATURE CONVERSION RESULTS")
        print("="*50)
        
        unit_symbols = {
            'celsius': '°C',
            'fahrenheit': '°F',
            'kelvin': ' K'
        }
        
        unit_colors = {
            'celsius': '🔵',
            'fahrenheit': '🔴',
            'kelvin': '🟣'
        }
        
        print(f"📊 Original: {original_value:.2f}{unit_symbols[original_unit]} ({original_unit.title()})")
        print("-" * 50)
        
        for unit, value in results.items():
            if unit != original_unit:
                color = unit_colors.get(unit, '⚪')
                print(f"{color} {unit.title()}: {value:.2f}{unit_symbols[unit]}")
        
        print("="*50)
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("🌡️  TEMPERATURE CONVERTER")
        print("="*50)
        print("Convert temperatures between:")
        print("• Celsius (°C)")
        print("• Fahrenheit (°F)")
        print("• Kelvin (K)")
        print("-" * 50)
        print("💡 Supported units: celsius, fahrenheit, kelvin")
        print("💡 Short forms: c, f, k")
        print("💡 Type 'quit' anytime to exit")
        print("="*50)
    
    def run(self):
        """Main program loop"""
        print("Welcome to the Temperature Converter! 🌡️")
        
        while True:
            self.show_menu()
            
            # Get temperature value
            temp_value = self.get_temperature_input()
            if temp_value is None:
                break
            
            # Get original unit
            from_unit = self.get_unit_input("Enter the original unit (celsius/fahrenheit/kelvin): ")
            if from_unit is None:
                break
            
            # Validate temperature
            is_valid, error_msg = self.validate_temperature(temp_value, from_unit)
            if not is_valid:
                print(f"❌ {error_msg}")
                continue
            
            # Convert temperatures
            results = self.convert_all_units(temp_value, from_unit)
            
            # Display results
            self.display_results(results, from_unit, temp_value)
            
            # Ask if user wants to continue
            while True:
                choice = input("\nWould you like to convert another temperature? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no', 'quit']:
                    print("\nThank you for using the Temperature Converter! 👋")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")

def main():
    """Main function to run the temperature converter"""
    converter = TemperatureConverterCLI()
    try:
        converter.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please restart the program.")

if __name__ == "__main__":
    main()
