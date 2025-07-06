# Contact Management System

A comprehensive contact management system with both GUI and CLI interfaces, featuring persistent storage, data validation, and import/export capabilities.

## Features

### Core Functionality
- **Add Contacts**: Create new contacts with name, phone, email, address, and notes
- **View Contacts**: Display all contacts in a user-friendly format
- **Edit Contacts**: Update existing contact information
- **Delete Contacts**: Remove contacts from the system
- **Search Contacts**: Find contacts by name, phone, or email
- **Persistent Storage**: Automatically save and load contacts using JSON format

### Advanced Features
- **Data Validation**: Ensures phone numbers and email addresses are properly formatted
- **Import/Export**: Backup and restore contacts using JSON files
- **Contact Statistics**: View summary information about your contacts
- **Timestamps**: Track when contacts were created and last modified
- **Duplicate Detection**: Prevent duplicate contacts based on phone numbers

### User Interfaces
- **GUI Version**: Modern tkinter-based interface with intuitive navigation
- **CLI Version**: Command-line interface for terminal users
- **Interactive Menus**: Easy-to-use menu systems in both versions

## Files

- `contact_manager.py` - GUI version with tkinter interface
- `contact_manager_cli.py` - Command-line interface version
- `test_demo.py` - Comprehensive testing and demonstration script
- `run_contacts.bat` - Windows batch launcher
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
python contact_manager.py
```

### CLI Version
```bash
python contact_manager_cli.py
```

### Using the Batch Launcher (Windows)
```bash
run_contacts.bat
```

### Running Tests and Demos
```bash
python test_demo.py
```

## GUI Interface Features

### Main Window
- **Contact List**: Displays all contacts with name, phone, and email
- **Add Contact**: Button to create new contacts
- **Edit Contact**: Modify selected contact information
- **Delete Contact**: Remove selected contacts
- **Search**: Find contacts quickly using the search functionality

### Contact Form
- **Name**: Required field for contact name
- **Phone**: Phone number with format validation
- **Email**: Email address with format validation
- **Address**: Optional address field
- **Notes**: Optional notes field

### Menu Options
- **File Menu**: Import, Export, Exit
- **Tools Menu**: Statistics, Clear Search
- **Help Menu**: About dialog

## CLI Interface Features

### Main Menu Options
1. **Add Contact**: Create a new contact with guided prompts
2. **View All Contacts**: Display all contacts in formatted table
3. **Search Contacts**: Find contacts by name, phone, or email
4. **Edit Contact**: Update existing contact information
5. **Delete Contact**: Remove contacts from the system
6. **Import Contacts**: Load contacts from JSON file
7. **Export Contacts**: Save contacts to JSON file
8. **Statistics**: View contact database statistics
9. **Exit**: Save and exit the application

### Search Functionality
- Search by partial name match
- Search by phone number
- Search by email address
- Case-insensitive search

## Data Storage

### JSON Format
Contacts are stored in `contacts.json` with the following structure:
```json
{
  "name": "John Doe",
  "phone": "1234567890",
  "email": "john@example.com",
  "address": "123 Main St",
  "notes": "Friend from college",
  "created_date": "2024-01-15 10:30:00",
  "modified_date": "2024-01-15 10:30:00"
}
```

### Automatic Backup
- Contacts are automatically saved after each operation
- Data persists between application runs
- Import/Export functionality for data backup and transfer

## Validation Rules

### Phone Numbers
- Must contain only digits, spaces, hyphens, and parentheses
- Common formats accepted: (123) 456-7890, 123-456-7890, 1234567890
- No duplicate phone numbers allowed

### Email Addresses
- Must contain @ symbol
- Must have valid domain format
- Basic email format validation

### Required Fields
- Name: Required, cannot be empty
- Phone: Required, must be valid format
- Email: Optional but validated if provided

## Testing

The `test_demo.py` script includes comprehensive tests for:

### Unit Tests
- Contact creation and validation
- Contact manager operations
- Data persistence
- Search functionality
- Import/export operations

### Integration Tests
- GUI component testing
- CLI menu testing
- File operations testing
- Error handling validation

### Demo Scenarios
- Adding sample contacts
- Performing search operations
- Testing import/export functionality
- Validating data persistence

## Error Handling

### Graceful Error Management
- Invalid input validation with user feedback
- File operation error handling
- JSON parsing error recovery
- User-friendly error messages

### Data Integrity
- Automatic data backup before operations
- Validation of imported data
- Recovery from corrupted data files

## Performance

### Optimizations
- Efficient search algorithms
- Minimal memory usage
- Fast JSON serialization
- Responsive GUI updates

### Scalability
- Handles hundreds of contacts efficiently
- Optimized for both small and large contact lists
- Memory-efficient data structures

## Development

### Code Structure
- **Contact Class**: Core data model with validation
- **ContactManager Class**: Business logic and data persistence
- **GUI Classes**: Tkinter interface components
- **CLI Functions**: Command-line interface handlers

### Best Practices
- Object-oriented design
- Separation of concerns
- Comprehensive error handling
- Clean, documented code

## Compatibility

- **Python Version**: 3.6+
- **Operating System**: Windows, macOS, Linux
- **GUI Framework**: tkinter (included with Python)
- **Dependencies**: Python standard library only

## Future Enhancements

### Planned Features
- Photo support for contacts
- Contact grouping and categories
- Advanced search filters
- CSV import/export
- Contact sharing functionality

### Extensibility
- Plugin architecture for custom fields
- Theme support for GUI
- Database backend option
- Web interface version

## License

This project is part of the PRODIGY InfoTech internship program and is intended for educational purposes.

## Support

For questions, issues, or suggestions, please refer to the main project documentation or contact the development team.

---

**Contact Management System** - Making contact organization simple and efficient! 📞✨
