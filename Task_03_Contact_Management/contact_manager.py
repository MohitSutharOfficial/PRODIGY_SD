import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.data_file = "contacts.json"
        self.load_contacts()
    
    def add_contact(self, contact):
        """Add a new contact"""
        self.contacts.append(contact)
        self.save_contacts()
    
    def remove_contact(self, index):
        """Remove a contact by index"""
        if 0 <= index < len(self.contacts):
            self.contacts.pop(index)
            self.save_contacts()
            return True
        return False
    
    def update_contact(self, index, **kwargs):
        """Update a contact by index"""
        if 0 <= index < len(self.contacts):
            self.contacts[index].update(**kwargs)
            self.save_contacts()
            return True
        return False
    
    def search_contacts(self, query):
        """Search contacts by name, phone, or email"""
        query = query.lower()
        results = []
        for i, contact in enumerate(self.contacts):
            if (query in contact.name.lower() or
                query in contact.phone or
                query in contact.email.lower() or
                query in contact.address.lower()):
                results.append((i, contact))
        return results
    
    def get_contact(self, index):
        """Get a contact by index"""
        if 0 <= index < len(self.contacts):
            return self.contacts[index]
        return None
    
    def get_all_contacts(self):
        """Get all contacts"""
        return self.contacts
    
    def save_contacts(self):
        """Save contacts to file"""
        try:
            data = [contact.to_dict() for contact in self.contacts]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving contacts: {e}")
    
    def load_contacts(self):
        """Load contacts from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.contacts = [Contact.from_dict(contact_data) for contact_data in data]
        except Exception as e:
            print(f"Error loading contacts: {e}")
            self.contacts = []
    
    def export_contacts(self, filename):
        """Export contacts to a file"""
        try:
            data = [contact.to_dict() for contact in self.contacts]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting contacts: {e}")
            return False
    
    def import_contacts(self, filename):
        """Import contacts from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            imported_contacts = [Contact.from_dict(contact_data) for contact_data in data]
            self.contacts.extend(imported_contacts)
            self.save_contacts()
            return len(imported_contacts)
        except Exception as e:
            print(f"Error importing contacts: {e}")
            return 0

class ContactManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize contact manager
        self.contact_manager = ContactManager()
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main interface
        self.create_widgets()
        self.refresh_contact_list()
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="📞 Contact Management System",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Contact list
        left_panel = tk.Frame(main_frame, bg='#f0f0f0')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = tk.Frame(left_panel, bg='#f0f0f0')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Search:", font=("Arial", 10), bg='#f0f0f0').pack(side='left')
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10))
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_contacts,
            bg='#3498db',
            fg='white',
            font=("Arial", 9)
        )
        search_btn.pack(side='right', padx=5)
        
        # Contact list
        list_frame = tk.Frame(left_panel, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True)
        
        tk.Label(list_frame, text="📋 Contact List", font=("Arial", 12, "bold"), bg='#f0f0f0').pack(anchor='w')
        
        # Treeview for contact list
        columns = ('Name', 'Phone', 'Email')
        self.contact_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define column headings
        self.contact_tree.heading('Name', text='Name')
        self.contact_tree.heading('Phone', text='Phone')
        self.contact_tree.heading('Email', text='Email')
        
        # Configure column widths
        self.contact_tree.column('Name', width=150)
        self.contact_tree.column('Phone', width=120)
        self.contact_tree.column('Email', width=180)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)
        
        self.contact_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.contact_tree.bind('<<TreeviewSelect>>', self.on_contact_select)
        
        # Right panel - Contact details and actions
        right_panel = tk.Frame(main_frame, bg='#f0f0f0')
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        
        # Contact details frame
        details_frame = tk.LabelFrame(
            right_panel,
            text="Contact Details",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        details_frame.pack(fill='x', pady=(0, 10))
        
        # Form fields
        self.create_form_fields(details_frame)
        
        # Action buttons frame
        actions_frame = tk.LabelFrame(
            right_panel,
            text="Actions",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        actions_frame.pack(fill='x', pady=(0, 10))
        
        self.create_action_buttons(actions_frame)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(
            right_panel,
            text="Statistics",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        stats_frame.pack(fill='x')
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Total Contacts: 0",
            font=("Arial", 10),
            bg='#f0f0f0'
        )
        self.stats_label.pack()
        
    def create_form_fields(self, parent):
        """Create form fields for contact details"""
        # Name
        tk.Label(parent, text="👤 Name:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        self.name_entry = tk.Entry(parent, font=("Arial", 10), width=30)
        self.name_entry.pack(fill='x', pady=(0, 10))
        
        # Phone
        tk.Label(parent, text="📞 Phone:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        self.phone_entry = tk.Entry(parent, font=("Arial", 10), width=30)
        self.phone_entry.pack(fill='x', pady=(0, 10))
        
        # Email
        tk.Label(parent, text="✉️ Email:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        self.email_entry = tk.Entry(parent, font=("Arial", 10), width=30)
        self.email_entry.pack(fill='x', pady=(0, 10))
        
        # Address
        tk.Label(parent, text="🏠 Address:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        self.address_text = tk.Text(parent, font=("Arial", 10), width=30, height=3)
        self.address_text.pack(fill='x', pady=(0, 10))
        
        # Notes
        tk.Label(parent, text="📝 Notes:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        self.notes_text = tk.Text(parent, font=("Arial", 10), width=30, height=3)
        self.notes_text.pack(fill='x', pady=(0, 10))
        
    def create_action_buttons(self, parent):
        """Create action buttons"""
        # Add contact
        add_btn = tk.Button(
            parent,
            text="➕ Add Contact",
            command=self.add_contact,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            width=20
        )
        add_btn.pack(pady=2)
        
        # Update contact
        update_btn = tk.Button(
            parent,
            text="✏️ Update Contact",
            command=self.update_contact,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            width=20
        )
        update_btn.pack(pady=2)
        
        # Delete contact
        delete_btn = tk.Button(
            parent,
            text="🗑️ Delete Contact",
            command=self.delete_contact,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 10, "bold"),
            width=20
        )
        delete_btn.pack(pady=2)
        
        # Clear form
        clear_btn = tk.Button(
            parent,
            text="🗑️ Clear Form",
            command=self.clear_form,
            bg='#95a5a6',
            fg='white',
            font=("Arial", 10),
            width=20
        )
        clear_btn.pack(pady=2)
        
        # Separator
        tk.Label(parent, text="", bg='#f0f0f0').pack(pady=5)
        
        # Export contacts
        export_btn = tk.Button(
            parent,
            text="📤 Export Contacts",
            command=self.export_contacts,
            bg='#f39c12',
            fg='white',
            font=("Arial", 10),
            width=20
        )
        export_btn.pack(pady=2)
        
        # Import contacts
        import_btn = tk.Button(
            parent,
            text="📥 Import Contacts",
            command=self.import_contacts,
            bg='#9b59b6',
            fg='white',
            font=("Arial", 10),
            width=20
        )
        import_btn.pack(pady=2)
        
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        # Remove spaces, hyphens, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]+', '', phone)
        # Check if it contains only digits and has reasonable length
        return cleaned.isdigit() and 7 <= len(cleaned) <= 15
    
    def add_contact(self):
        """Add a new contact"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        # Validation
        if not name:
            messagebox.showerror("Validation Error", "Name is required!")
            return
        
        if not phone:
            messagebox.showerror("Validation Error", "Phone number is required!")
            return
        
        if not self.validate_phone(phone):
            messagebox.showerror("Validation Error", "Please enter a valid phone number!")
            return
        
        if email and not self.validate_email(email):
            messagebox.showerror("Validation Error", "Please enter a valid email address!")
            return
        
        # Check for duplicate names
        existing_names = [contact.name.lower() for contact in self.contact_manager.get_all_contacts()]
        if name.lower() in existing_names:
            if not messagebox.askyesno("Duplicate Name", f"A contact with the name '{name}' already exists. Do you want to add it anyway?"):
                return
        
        # Create and add contact
        contact = Contact(name, phone, email, address, notes)
        self.contact_manager.add_contact(contact)
        
        # Refresh UI
        self.refresh_contact_list()
        self.clear_form()
        
        messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
        
    def update_contact(self):
        """Update selected contact"""
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a contact to update!")
            return
        
        # Get contact index
        index = self.contact_tree.index(selected_item[0])
        
        # Get form data
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        # Validation
        if not name:
            messagebox.showerror("Validation Error", "Name is required!")
            return
        
        if not phone:
            messagebox.showerror("Validation Error", "Phone number is required!")
            return
        
        if not self.validate_phone(phone):
            messagebox.showerror("Validation Error", "Please enter a valid phone number!")
            return
        
        if email and not self.validate_email(email):
            messagebox.showerror("Validation Error", "Please enter a valid email address!")
            return
        
        # Update contact
        self.contact_manager.update_contact(index, name=name, phone=phone, email=email, address=address, notes=notes)
        
        # Refresh UI
        self.refresh_contact_list()
        self.clear_form()
        
        messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
        
    def delete_contact(self):
        """Delete selected contact"""
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a contact to delete!")
            return
        
        # Get contact info
        index = self.contact_tree.index(selected_item[0])
        contact = self.contact_manager.get_contact(index)
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{contact.name}'?"):
            self.contact_manager.remove_contact(index)
            self.refresh_contact_list()
            self.clear_form()
            messagebox.showinfo("Success", f"Contact '{contact.name}' deleted successfully!")
        
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
        self.notes_text.delete("1.0", tk.END)
        
    def on_contact_select(self, event):
        """Handle contact selection"""
        selected_item = self.contact_tree.selection()
        if selected_item:
            index = self.contact_tree.index(selected_item[0])
            contact = self.contact_manager.get_contact(index)
            
            # Populate form fields
            self.clear_form()
            self.name_entry.insert(0, contact.name)
            self.phone_entry.insert(0, contact.phone)
            self.email_entry.insert(0, contact.email)
            self.address_text.insert("1.0", contact.address)
            self.notes_text.insert("1.0", contact.notes)
            
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        # Clear current items
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        # Add all contacts
        for contact in self.contact_manager.get_all_contacts():
            self.contact_tree.insert('', 'end', values=(contact.name, contact.phone, contact.email))
        
        # Update statistics
        total_contacts = len(self.contact_manager.get_all_contacts())
        self.stats_label.config(text=f"Total Contacts: {total_contacts}")
        
    def search_contacts(self):
        """Search contacts based on search query"""
        query = self.search_entry.get().strip()
        if not query:
            self.refresh_contact_list()
            return
        
        # Clear current items
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        # Search and display results
        results = self.contact_manager.search_contacts(query)
        for index, contact in results:
            self.contact_tree.insert('', 'end', values=(contact.name, contact.phone, contact.email))
        
        # Update statistics
        self.stats_label.config(text=f"Search Results: {len(results)} contacts")
        
    def on_search(self, event):
        """Handle search as user types"""
        # Add small delay to avoid too many searches
        if hasattr(self, 'search_timer'):
            self.root.after_cancel(self.search_timer)
        self.search_timer = self.root.after(300, self.search_contacts)
        
    def export_contacts(self):
        """Export contacts to a file"""
        if not self.contact_manager.get_all_contacts():
            messagebox.showwarning("No Contacts", "No contacts to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Contacts"
        )
        
        if filename:
            if self.contact_manager.export_contacts(filename):
                messagebox.showinfo("Success", f"Contacts exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export contacts!")
                
    def import_contacts(self):
        """Import contacts from a file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Contacts"
        )
        
        if filename:
            imported_count = self.contact_manager.import_contacts(filename)
            if imported_count > 0:
                self.refresh_contact_list()
                messagebox.showinfo("Success", f"Imported {imported_count} contacts!")
            else:
                messagebox.showerror("Error", "Failed to import contacts!")

def main():
    root = tk.Tk()
    app = ContactManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
