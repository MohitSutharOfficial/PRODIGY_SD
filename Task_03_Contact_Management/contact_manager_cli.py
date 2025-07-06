"""
Contact Management System - Command Line Version
A comprehensive CLI-based contact management system with persistent storage.
"""

import json
import os
import re
from datetime import datetime

class Contact:
    def __init__(self, name, phone, email, address="", notes=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.modified_date = self.created_date
    
    def to_dict(self):
        """Convert contact to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'notes': self.notes,
            'created_date': self.created_date,
            'modified_date': self.modified_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create contact from dictionary"""
        contact = cls(
            data['name'],
            data['phone'],
            data['email'],
            data.get('address', ''),
            data.get('notes', '')
        )
        contact.created_date = data.get('created_date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        contact.modified_date = data.get('modified_date', contact.created_date)
        return contact
    
    def update(self, name=None, phone=None, email=None, address=None, notes=None):
        """Update contact information"""
        if name is not None:
            self.name = name
        if phone is not None:
            self.phone = phone
        if email is not None:
            self.email = email
        if address is not None:
            self.address = address
        if notes is not None:
            self.notes = notes
        self.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        return f"{self.name} - {self.phone} - {self.email}"

class ContactManagerCLI:
    def __init__(self):
        self.contacts = []
        self.data_file = "contacts.json"
        self.load_contacts()
    
    def validate_email(self, email):
        """Validate email format"""
        if not email:
            return True  # Email is optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        if not phone:
            return False  # Phone is required
        # Remove spaces, hyphens, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]+', '', phone)
        # Check if it contains only digits and has reasonable length
        return cleaned.isdigit() and 7 <= len(cleaned) <= 15
    
    def add_contact(self):
        """Add a new contact"""
        print("\n➕ Adding New Contact")
        print("=" * 40)
        
        # Get contact information
        name = input("👤 Name (required): ").strip()
        if not name:
            print("❌ Name is required!")
            return
        
        phone = input("📞 Phone (required): ").strip()
        if not phone:
            print("❌ Phone number is required!")
            return
        
        if not self.validate_phone(phone):
            print("❌ Please enter a valid phone number!")
            return
        
        email = input("✉️ Email (optional): ").strip()
        if email and not self.validate_email(email):
            print("❌ Please enter a valid email address!")
            return
        
        address = input("🏠 Address (optional): ").strip()
        notes = input("📝 Notes (optional): ").strip()
        
        # Check for duplicate names
        existing_names = [contact.name.lower() for contact in self.contacts]
        if name.lower() in existing_names:
            choice = input(f"⚠️  A contact with the name '{name}' already exists. Add anyway? (y/n): ")
            if choice.lower() != 'y':
                return
        
        # Create and add contact
        contact = Contact(name, phone, email, address, notes)
        self.contacts.append(contact)
        self.save_contacts()
        
        print(f"✅ Contact '{name}' added successfully!")
        
    def view_contacts(self):
        """View all contacts"""
        if not self.contacts:
            print("\n📋 No contacts found!")
            return
        
        print(f"\n📋 Contact List ({len(self.contacts)} contacts)")
        print("=" * 80)
        
        for i, contact in enumerate(self.contacts, 1):
            print(f"{i:2d}. 👤 {contact.name}")
            print(f"    📞 {contact.phone}")
            if contact.email:
                print(f"    ✉️  {contact.email}")
            if contact.address:
                print(f"    🏠 {contact.address}")
            if contact.notes:
                print(f"    📝 {contact.notes}")
            print(f"    📅 Created: {contact.created_date}")
            if contact.modified_date != contact.created_date:
                print(f"    ✏️  Modified: {contact.modified_date}")
            print("-" * 80)
    
    def search_contacts(self):
        """Search contacts"""
        query = input("\n🔍 Enter search term (name, phone, email, or address): ").strip()
        if not query:
            print("❌ Search term cannot be empty!")
            return
        
        results = []
        query_lower = query.lower()
        
        for i, contact in enumerate(self.contacts):
            if (query_lower in contact.name.lower() or
                query in contact.phone or
                query_lower in contact.email.lower() or
                query_lower in contact.address.lower()):
                results.append((i, contact))
        
        if not results:
            print(f"🔍 No contacts found matching '{query}'")
            return
        
        print(f"\n🔍 Search Results ({len(results)} found)")
        print("=" * 80)
        
        for index, contact in results:
            print(f"{index + 1:2d}. 👤 {contact.name}")
            print(f"    📞 {contact.phone}")
            if contact.email:
                print(f"    ✉️  {contact.email}")
            if contact.address:
                print(f"    🏠 {contact.address}")
            if contact.notes:
                print(f"    📝 {contact.notes}")
            print("-" * 80)
    
    def edit_contact(self):
        """Edit an existing contact"""
        if not self.contacts:
            print("\n📋 No contacts to edit!")
            return
        
        self.view_contacts()
        
        try:
            index = int(input(f"\n✏️ Enter contact number to edit (1-{len(self.contacts)}): ")) - 1
            if 0 <= index < len(self.contacts):
                contact = self.contacts[index]
                
                print(f"\n✏️ Editing Contact: {contact.name}")
                print("=" * 40)
                print("💡 Press Enter to keep current value")
                
                # Get new values
                new_name = input(f"👤 Name [{contact.name}]: ").strip()
                if not new_name:
                    new_name = contact.name
                
                new_phone = input(f"📞 Phone [{contact.phone}]: ").strip()
                if not new_phone:
                    new_phone = contact.phone
                elif not self.validate_phone(new_phone):
                    print("❌ Invalid phone number! Keeping original.")
                    new_phone = contact.phone
                
                new_email = input(f"✉️ Email [{contact.email}]: ").strip()
                if new_email and not self.validate_email(new_email):
                    print("❌ Invalid email! Keeping original.")
                    new_email = contact.email
                elif new_email == "":
                    new_email = contact.email
                
                new_address = input(f"🏠 Address [{contact.address}]: ").strip()
                if new_address == "":
                    new_address = contact.address
                
                new_notes = input(f"📝 Notes [{contact.notes}]: ").strip()
                if new_notes == "":
                    new_notes = contact.notes
                
                # Update contact
                contact.update(new_name, new_phone, new_email, new_address, new_notes)
                self.save_contacts()
                
                print(f"✅ Contact '{contact.name}' updated successfully!")
            else:
                print("❌ Invalid contact number!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def delete_contact(self):
        """Delete a contact"""
        if not self.contacts:
            print("\n📋 No contacts to delete!")
            return
        
        self.view_contacts()
        
        try:
            index = int(input(f"\n🗑️ Enter contact number to delete (1-{len(self.contacts)}): ")) - 1
            if 0 <= index < len(self.contacts):
                contact = self.contacts[index]
                
                confirm = input(f"⚠️  Are you sure you want to delete '{contact.name}'? (y/n): ")
                if confirm.lower() == 'y':
                    deleted_contact = self.contacts.pop(index)
                    self.save_contacts()
                    print(f"✅ Contact '{deleted_contact.name}' deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid contact number!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def save_contacts(self):
        """Save contacts to file"""
        try:
            data = [contact.to_dict() for contact in self.contacts]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving contacts: {e}")
    
    def load_contacts(self):
        """Load contacts from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.contacts = [Contact.from_dict(contact_data) for contact_data in data]
                print(f"✅ Loaded {len(self.contacts)} contacts from {self.data_file}")
            else:
                print(f"📁 No existing contact file found. Starting fresh.")
        except Exception as e:
            print(f"❌ Error loading contacts: {e}")
            self.contacts = []
    
    def export_contacts(self):
        """Export contacts to a file"""
        if not self.contacts:
            print("\n📋 No contacts to export!")
            return
        
        filename = input("📤 Enter filename to export to (with .json extension): ").strip()
        if not filename:
            filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            data = [contact.to_dict() for contact in self.contacts]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ {len(self.contacts)} contacts exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting contacts: {e}")
    
    def import_contacts(self):
        """Import contacts from a file"""
        filename = input("📥 Enter filename to import from: ").strip()
        if not filename:
            print("❌ Filename cannot be empty!")
            return
        
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found!")
            return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            imported_contacts = [Contact.from_dict(contact_data) for contact_data in data]
            
            # Ask about duplicates
            if self.contacts:
                choice = input(f"⚠️  You have {len(self.contacts)} existing contacts. Merge with imports? (y/n): ")
                if choice.lower() != 'y':
                    choice = input("❓ Replace all existing contacts? (y/n): ")
                    if choice.lower() == 'y':
                        self.contacts = imported_contacts
                    else:
                        print("❌ Import cancelled.")
                        return
                else:
                    self.contacts.extend(imported_contacts)
            else:
                self.contacts = imported_contacts
            
            self.save_contacts()
            print(f"✅ {len(imported_contacts)} contacts imported successfully!")
            
        except Exception as e:
            print(f"❌ Error importing contacts: {e}")
    
    def show_statistics(self):
        """Show contact statistics"""
        if not self.contacts:
            print("\n📊 No contacts to analyze!")
            return
        
        print(f"\n📊 Contact Statistics")
        print("=" * 40)
        print(f"📞 Total Contacts: {len(self.contacts)}")
        
        # Count contacts with email
        with_email = sum(1 for contact in self.contacts if contact.email)
        print(f"✉️  Contacts with Email: {with_email}")
        
        # Count contacts with address
        with_address = sum(1 for contact in self.contacts if contact.address)
        print(f"🏠 Contacts with Address: {with_address}")
        
        # Count contacts with notes
        with_notes = sum(1 for contact in self.contacts if contact.notes)
        print(f"📝 Contacts with Notes: {with_notes}")
        
        # Recent contacts (last 7 days)
        recent_count = 0
        for contact in self.contacts:
            try:
                created_date = datetime.strptime(contact.created_date, "%Y-%m-%d %H:%M:%S")
                days_ago = (datetime.now() - created_date).days
                if days_ago <= 7:
                    recent_count += 1
            except:
                pass
        
        print(f"🆕 Recently Added (7 days): {recent_count}")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 50)
        print("📞 CONTACT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. ➕ Add New Contact")
        print("2. 📋 View All Contacts")
        print("3. 🔍 Search Contacts")
        print("4. ✏️ Edit Contact")
        print("5. 🗑️ Delete Contact")
        print("6. 📤 Export Contacts")
        print("7. 📥 Import Contacts")
        print("8. 📊 Show Statistics")
        print("9. 🚪 Exit")
        print("=" * 50)
    
    def run(self):
        """Main program loop"""
        print("🎉 Welcome to the Contact Management System!")
        
        while True:
            try:
                self.display_menu()
                choice = input("👉 Enter your choice (1-9): ").strip()
                
                if choice == '1':
                    self.add_contact()
                elif choice == '2':
                    self.view_contacts()
                elif choice == '3':
                    self.search_contacts()
                elif choice == '4':
                    self.edit_contact()
                elif choice == '5':
                    self.delete_contact()
                elif choice == '6':
                    self.export_contacts()
                elif choice == '7':
                    self.import_contacts()
                elif choice == '8':
                    self.show_statistics()
                elif choice == '9':
                    print("\n👋 Thank you for using Contact Management System!")
                    print("💾 All contacts have been saved automatically.")
                    break
                else:
                    print("❌ Invalid choice! Please enter a number between 1-9.")
                
                # Pause before showing menu again
                if choice != '9':
                    input("\n⏸️  Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using Contact Management System!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("🔄 Please try again.")

def main():
    """Main function to run the contact management system"""
    contact_manager = ContactManagerCLI()
    contact_manager.run()

if __name__ == "__main__":
    main()
