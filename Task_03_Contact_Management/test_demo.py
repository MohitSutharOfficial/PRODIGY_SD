"""
Test and Demo Script for the Contact Management System
This script demonstrates and tests the core contact management functions
"""

import json
import os
import tempfile
import shutil
from datetime import datetime

def test_contact_creation():
    """Test contact creation and basic operations"""
    print("🧪 Testing Contact Creation and Operations")
    print("=" * 50)
    
    # Import the Contact class
    from contact_manager_cli import Contact
    
    test_cases = [
        ("John Doe", "1234567890", "john@example.com", "123 Main St", "Friend"),
        ("Jane Smith", "0987654321", "jane@example.com", "", ""),
        ("Bob Johnson", "5555551234", "", "456 Oak Ave", "Colleague"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for name, phone, email, address, notes in test_cases:
        try:
            # Create contact
            contact = Contact(name, phone, email, address, notes)
            
            # Test basic properties
            if (contact.name == name and 
                contact.phone == phone and 
                contact.email == email and 
                contact.address == address and 
                contact.notes == notes):
                
                print(f"✅ PASSED - Contact '{name}' created successfully")
                passed += 1
            else:
                print(f"❌ FAILED - Contact '{name}' properties don't match")
                
        except Exception as e:
            print(f"❌ FAILED - Error creating contact '{name}': {e}")
    
    print(f"\n📊 Contact Creation Test Results: {passed}/{total} passed")
    return passed == total

def test_json_serialization():
    """Test JSON serialization and deserialization"""
    print("\n🧪 Testing JSON Serialization")
    print("=" * 50)
    
    from contact_manager_cli import Contact
    
    # Create test contact
    original = Contact(
        "Test User",
        "1234567890",
        "test@example.com",
        "123 Test St",
        "Test contact"
    )
    
    try:
        # Convert to dict
        contact_dict = original.to_dict()
        
        # Convert back from dict
        restored = Contact.from_dict(contact_dict)
        
        # Check if all properties match
        if (original.name == restored.name and
            original.phone == restored.phone and
            original.email == restored.email and
            original.address == restored.address and
            original.notes == restored.notes):
            
            print("✅ PASSED - JSON serialization works correctly")
            return True
        else:
            print("❌ FAILED - Restored contact doesn't match original")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Error in serialization: {e}")
        return False

def test_validation_functions():
    """Test email and phone validation"""
    print("\n🧪 Testing Validation Functions")
    print("=" * 50)
    
    from contact_manager_cli import ContactManagerCLI
    
    manager = ContactManagerCLI()
    manager.contacts = []  # Start with empty list for testing
    
    # Email validation tests
    email_tests = [
        ("user@example.com", True),
        ("test.email@domain.co.uk", True),
        ("user+tag@example.org", True),
        ("invalid-email", False),
        ("@example.com", False),
        ("user@", False),
        ("", True),  # Empty email should be valid (optional)
    ]
    
    print("📧 Testing Email Validation:")
    email_passed = 0
    for email, expected in email_tests:
        result = manager.validate_email(email)
        if result == expected:
            status = "✅ PASSED"
            email_passed += 1
        else:
            status = "❌ FAILED"
        print(f"  {email or '(empty)'}: {status}")
    
    # Phone validation tests
    phone_tests = [
        ("1234567890", True),
        ("123-456-7890", True),
        ("(123) 456-7890", True),
        ("123 456 7890", True),
        ("12345", False),  # Too short
        ("123456789012345678", False),  # Too long
        ("abc1234567", False),  # Contains letters
        ("", False),  # Empty phone should be invalid (required)
    ]
    
    print("\n📞 Testing Phone Validation:")
    phone_passed = 0
    for phone, expected in phone_tests:
        result = manager.validate_phone(phone)
        if result == expected:
            status = "✅ PASSED"
            phone_passed += 1
        else:
            status = "❌ FAILED"
        print(f"  '{phone}': {status}")
    
    total_tests = len(email_tests) + len(phone_tests)
    total_passed = email_passed + phone_passed
    
    print(f"\n📊 Validation Test Results: {total_passed}/{total_tests} passed")
    return total_passed == total_tests

def test_file_operations():
    """Test file save and load operations"""
    print("\n🧪 Testing File Operations")
    print("=" * 50)
    
    from contact_manager_cli import Contact, ContactManagerCLI
    
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_contacts.json")
    
    try:
        # Create test contacts
        test_contacts = [
            Contact("Alice", "1111111111", "alice@test.com", "111 First St", "Test 1"),
            Contact("Bob", "2222222222", "bob@test.com", "222 Second St", "Test 2"),
            Contact("Charlie", "3333333333", "charlie@test.com", "333 Third St", "Test 3"),
        ]
        
        # Create manager and set custom file
        manager = ContactManagerCLI()
        manager.data_file = temp_file
        manager.contacts = test_contacts
        
        # Test save
        manager.save_contacts()
        
        if os.path.exists(temp_file):
            print("✅ PASSED - File save operation")
        else:
            print("❌ FAILED - File was not created")
            return False
        
        # Test load
        new_manager = ContactManagerCLI()
        new_manager.data_file = temp_file
        new_manager.load_contacts()
        
        if len(new_manager.contacts) == len(test_contacts):
            print("✅ PASSED - File load operation")
            
            # Check if contacts match
            all_match = True
            for i, contact in enumerate(new_manager.contacts):
                original = test_contacts[i]
                if (contact.name != original.name or
                    contact.phone != original.phone or
                    contact.email != original.email):
                    all_match = False
                    break
            
            if all_match:
                print("✅ PASSED - Contact data integrity")
                return True
            else:
                print("❌ FAILED - Contact data doesn't match")
                return False
        else:
            print("❌ FAILED - Wrong number of contacts loaded")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Error in file operations: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def demo_contact_operations():
    """Demonstrate contact management operations"""
    print("\n🎮 Contact Management Demo")
    print("=" * 50)
    
    from contact_manager_cli import Contact, ContactManagerCLI
    
    # Create demo manager
    manager = ContactManagerCLI()
    original_file = manager.data_file
    manager.data_file = "demo_contacts.json"
    manager.contacts = []  # Start fresh for demo
    
    try:
        print("📝 Creating sample contacts...")
        
        # Create sample contacts
        demo_contacts = [
            Contact("Alice Johnson", "555-0101", "alice.johnson@email.com", "123 Maple Street", "College friend"),
            Contact("Bob Smith", "555-0102", "bob.smith@company.com", "456 Oak Avenue", "Work colleague"),
            Contact("Carol Wilson", "555-0103", "carol.w@example.org", "789 Pine Road", "Neighbor"),
            Contact("David Brown", "555-0104", "", "321 Elm Street", "Family friend"),
            Contact("Emma Davis", "555-0105", "emma.davis@university.edu", "", "Study group"),
        ]
        
        for contact in demo_contacts:
            manager.contacts.append(contact)
        
        print(f"✅ Created {len(demo_contacts)} sample contacts")
        
        # Save contacts
        manager.save_contacts()
        print("💾 Contacts saved to file")
        
        # Demo search functionality
        print("\n🔍 Testing search functionality:")
        search_results = []
        
        # Search by name
        for i, contact in enumerate(manager.contacts):
            if "alice" in contact.name.lower():
                search_results.append((i, contact))
        
        print(f"📋 Found {len(search_results)} contacts matching 'alice':")
        for index, contact in search_results:
            print(f"  - {contact.name} ({contact.phone})")
        
        # Demo statistics
        print(f"\n📊 Contact Statistics:")
        total = len(manager.contacts)
        with_email = sum(1 for c in manager.contacts if c.email)
        with_address = sum(1 for c in manager.contacts if c.address)
        with_notes = sum(1 for c in manager.contacts if c.notes)
        
        print(f"  Total Contacts: {total}")
        print(f"  With Email: {with_email}")
        print(f"  With Address: {with_address}")
        print(f"  With Notes: {with_notes}")
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        # Clean up demo file
        if os.path.exists(manager.data_file):
            os.remove(manager.data_file)
        manager.data_file = original_file

def demo_gui():
    """Demo the GUI version"""
    print("\n🖥️ Starting GUI Demo...")
    print("💡 The GUI window will open shortly.")
    print("💡 Try adding, editing, and searching contacts!")
    
    try:
        import contact_manager
        contact_manager.main()
    except ImportError as e:
        print(f"❌ Could not import GUI version: {e}")
    except Exception as e:
        print(f"❌ Error running GUI: {e}")

def demo_cli():
    """Demo the CLI version"""
    print("\n💻 Starting CLI Demo...")
    print("💡 This will start the command-line interface.")
    
    try:
        import contact_manager_cli
        contact_manager_cli.main()
    except ImportError as e:
        print(f"❌ Could not import CLI version: {e}")
    except Exception as e:
        print(f"❌ Error running CLI: {e}")

def run_all_tests():
    """Run all test functions"""
    print("🧪 Running All Tests for Contact Management System")
    print("=" * 60)
    
    test_results = []
    
    # Run tests
    test_results.append(("Contact Creation", test_contact_creation()))
    test_results.append(("JSON Serialization", test_json_serialization()))
    test_results.append(("Validation Functions", test_validation_functions()))
    test_results.append(("File Operations", test_file_operations()))
    
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
        print("\n🎉 All tests passed! The contact management system is ready!")
    else:
        print("\n⚠️  Some tests failed. Please review the implementation.")

def create_sample_data():
    """Create sample contact data for testing"""
    print("\n📝 Creating Sample Contact Data")
    print("=" * 50)
    
    from contact_manager_cli import Contact, ContactManagerCLI
    
    # Create sample contacts
    sample_contacts = [
        Contact("John Doe", "555-0101", "john.doe@email.com", "123 Main Street, Anytown, USA", "Best friend from college"),
        Contact("Jane Smith", "555-0102", "jane.smith@company.com", "456 Business Ave, Corporate City", "Project manager at work"),
        Contact("Mike Johnson", "555-0103", "mike.j@example.org", "789 Residential Blvd", "Neighbor next door"),
        Contact("Sarah Wilson", "555-0104", "sarah.wilson@university.edu", "321 Campus Drive", "Study group partner"),
        Contact("Tom Brown", "555-0105", "", "654 Family Lane", "Cousin from out of town"),
        Contact("Lisa Davis", "555-0106", "lisa.davis@clinic.com", "987 Health Street", "Family doctor"),
        Contact("Robert Garcia", "555-0107", "r.garcia@services.net", "", "Plumber - emergency contact"),
        Contact("Emily Chen", "555-0108", "emily.chen@startup.io", "159 Innovation Hub", "Entrepreneur friend"),
    ]
    
    # Save to file
    manager = ContactManagerCLI()
    manager.contacts = sample_contacts
    manager.data_file = "sample_contacts.json"
    manager.save_contacts()
    
    print(f"✅ Created {len(sample_contacts)} sample contacts")
    print(f"💾 Saved to {manager.data_file}")
    print("💡 You can import this file in the main application")

def main():
    """Main function to run tests and demos"""
    print("📞 Contact Management System - Test & Demo Script")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Run all tests")
        print("2. Demo contact operations")
        print("3. Demo GUI version")
        print("4. Demo CLI version")
        print("5. Test contact creation")
        print("6. Test JSON serialization")
        print("7. Test validation functions")
        print("8. Test file operations")
        print("9. Create sample data")
        print("10. Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == '1':
            run_all_tests()
        elif choice == '2':
            demo_contact_operations()
        elif choice == '3':
            demo_gui()
        elif choice == '4':
            demo_cli()
        elif choice == '5':
            test_contact_creation()
        elif choice == '6':
            test_json_serialization()
        elif choice == '7':
            test_validation_functions()
        elif choice == '8':
            test_file_operations()
        elif choice == '9':
            create_sample_data()
        elif choice == '10':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-10.")

if __name__ == "__main__":
    main()
