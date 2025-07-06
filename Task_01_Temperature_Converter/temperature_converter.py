"""
Temperature Converter Application
A simple GUI application for converting temperatures between Celsius, Fahrenheit, and Kelvin.
Built for the PRODIGY Software Development Internship.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

class TemperatureConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Converter")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Temperature Converter", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Input section
        input_frame = tk.LabelFrame(
            main_frame, 
            text="Input Temperature", 
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333',
            padx=10,
            pady=10
        )
        input_frame.pack(fill='x', pady=10)
        
        # Temperature input
        tk.Label(
            input_frame, 
            text="Temperature Value:", 
            font=("Arial", 10),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.temp_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        self.temp_entry.grid(row=0, column=1, padx=10, pady=5)
        self.temp_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Unit selection
        tk.Label(
            input_frame, 
            text="From Unit:", 
            font=("Arial", 10),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.from_unit = ttk.Combobox(
            input_frame, 
            values=["Celsius", "Fahrenheit", "Kelvin"],
            state="readonly",
            font=("Arial", 10),
            width=12
        )
        self.from_unit.grid(row=1, column=1, padx=10, pady=5)
        self.from_unit.set("Celsius")
        self.from_unit.bind('<<ComboboxSelected>>', self.on_unit_change)
        
        # Convert button
        convert_btn = tk.Button(
            input_frame,
            text="Convert",
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            cursor='hand2',
            command=self.convert_temperature
        )
        convert_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Results section
        results_frame = tk.LabelFrame(
            main_frame, 
            text="Conversion Results", 
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333',
            padx=10,
            pady=10
        )
        results_frame.pack(fill='both', expand=True, pady=10)
        
        # Result labels
        self.celsius_result = tk.Label(
            results_frame, 
            text="Celsius: --", 
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        self.celsius_result.pack(pady=5, anchor='w')
        
        self.fahrenheit_result = tk.Label(
            results_frame, 
            text="Fahrenheit: --", 
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#FF9800'
        )
        self.fahrenheit_result.pack(pady=5, anchor='w')
        
        self.kelvin_result = tk.Label(
            results_frame, 
            text="Kelvin: --", 
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#9C27B0'
        )
        self.kelvin_result.pack(pady=5, anchor='w')
        
        # Clear button
        clear_btn = tk.Button(
            main_frame,
            text="Clear All",
            font=("Arial", 10),
            bg='#f44336',
            fg='white',
            cursor='hand2',
            command=self.clear_all
        )
        clear_btn.pack(pady=10)
        
        # Information section
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(fill='x', pady=10)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Tip: Enter a temperature value and select the unit to see conversions",
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666666'
        )
        info_text.pack()
        
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
    
    def validate_input(self, value, unit):
        """Validate temperature input based on unit"""
        if unit == "Kelvin" and value < 0:
            return False, "Kelvin temperature cannot be negative (absolute zero is 0 K)"
        elif unit == "Celsius" and value < -273.15:
            return False, "Celsius temperature cannot be below -273.15°C (absolute zero)"
        elif unit == "Fahrenheit" and value < -459.67:
            return False, "Fahrenheit temperature cannot be below -459.67°F (absolute zero)"
        return True, ""
    
    def convert_temperature(self):
        """Convert temperature based on input unit"""
        try:
            temp_value = float(self.temp_entry.get())
            from_unit = self.from_unit.get()
            
            # Validate input
            is_valid, error_msg = self.validate_input(temp_value, from_unit)
            if not is_valid:
                messagebox.showerror("Invalid Input", error_msg)
                return
            
            # Convert to all units
            if from_unit == "Celsius":
                celsius = temp_value
                fahrenheit = self.celsius_to_fahrenheit(celsius)
                kelvin = self.celsius_to_kelvin(celsius)
            elif from_unit == "Fahrenheit":
                fahrenheit = temp_value
                celsius = self.fahrenheit_to_celsius(fahrenheit)
                kelvin = self.fahrenheit_to_kelvin(fahrenheit)
            else:  # Kelvin
                kelvin = temp_value
                celsius = self.kelvin_to_celsius(kelvin)
                fahrenheit = self.kelvin_to_fahrenheit(kelvin)
            
            # Update result labels
            self.celsius_result.config(text=f"Celsius: {celsius:.2f}°C")
            self.fahrenheit_result.config(text=f"Fahrenheit: {fahrenheit:.2f}°F")
            self.kelvin_result.config(text=f"Kelvin: {kelvin:.2f} K")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def on_input_change(self, event):
        """Handle input change events"""
        # Auto-convert if there's a valid input
        if self.temp_entry.get().strip():
            try:
                float(self.temp_entry.get())
                self.convert_temperature()
            except ValueError:
                pass  # Ignore invalid input during typing
    
    def on_unit_change(self, event):
        """Handle unit selection change"""
        if self.temp_entry.get().strip():
            self.convert_temperature()
    
    def clear_all(self):
        """Clear all inputs and results"""
        self.temp_entry.delete(0, tk.END)
        self.from_unit.set("Celsius")
        self.celsius_result.config(text="Celsius: --")
        self.fahrenheit_result.config(text="Fahrenheit: --")
        self.kelvin_result.config(text="Kelvin: --")
        self.temp_entry.focus()

def main():
    root = tk.Tk()
    app = TemperatureConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
