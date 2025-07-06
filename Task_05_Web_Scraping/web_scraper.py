"""
Web Scraping Tool - GUI Version
A comprehensive web scraping tool for extracting product information from e-commerce websites.
Developed with ethical scraping practices and multiple export formats.

Features:
- Multi-website support
- Real-time progress tracking
- Robots.txt compliance
- Multiple export formats
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import re
import time
import threading
from datetime import datetime
import urllib.parse
from urllib.robotparser import RobotFileParser
import os
import sys

class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraping Tool - Product Information Extractor")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Data storage
        self.scraped_data = []
        self.current_url = ""
        self.scraping_active = False
        self.stop_scraping = False
        
        # Request session for better performance
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🕷️ Web Scraping Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="Target Website", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Preset URLs
        preset_frame = ttk.Frame(url_frame)
        preset_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(preset_frame, text="Quick Select:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        preset_buttons = [
            ("Books.toscrape.com", "http://books.toscrape.com/"),
            ("Quotes.toscrape.com", "http://quotes.toscrape.com/"),
            ("Example Store", "https://scrapeme.live/shop/")
        ]
        
        for i, (name, url) in enumerate(preset_buttons):
            btn = ttk.Button(preset_frame, text=name, 
                           command=lambda u=url: self.url_var.set(u))
            btn.grid(row=0, column=i+1, padx=(5, 0))
        
        # Scraping Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Scraping Configuration", padding="10")
        config_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Website type selection
        ttk.Label(config_frame, text="Website Type:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.website_type_var = tk.StringVar(value="books")
        website_combo = ttk.Combobox(config_frame, textvariable=self.website_type_var, 
                                   values=["books", "quotes", "general"], state="readonly")
        website_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Max pages
        ttk.Label(config_frame, text="Max Pages:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.max_pages_var = tk.StringVar(value="5")
        max_pages_entry = ttk.Entry(config_frame, textvariable=self.max_pages_var, width=10)
        max_pages_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        # Delay between requests
        ttk.Label(config_frame, text="Delay (seconds):").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.delay_var = tk.StringVar(value="1.0")
        delay_entry = ttk.Entry(config_frame, textvariable=self.delay_var, width=10)
        delay_entry.grid(row=0, column=5, sticky=tk.W)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Scraping", 
                                      command=self.start_scraping)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="🛑 Stop Scraping", 
                                     command=self.stop_scraping_process, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Clear Data", 
                                      command=self.clear_data)
        self.clear_button.grid(row=0, column=2, padx=(0, 10))
        
        self.export_button = ttk.Button(button_frame, text="💾 Export Data", 
                                       command=self.export_data)
        self.export_button.grid(row=0, column=3, padx=(0, 10))
        
        self.robots_button = ttk.Button(button_frame, text="🤖 Check Robots.txt", 
                                       command=self.check_robots_txt)
        self.robots_button.grid(row=0, column=4, padx=(0, 10))
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_var = tk.StringVar(value="Ready to scrape")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Statistics
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.items_count_var = tk.StringVar(value="Items: 0")
        self.pages_count_var = tk.StringVar(value="Pages: 0")
        self.time_elapsed_var = tk.StringVar(value="Time: 0s")
        
        ttk.Label(stats_frame, textvariable=self.items_count_var).grid(row=0, column=0, padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.pages_count_var).grid(row=0, column=1, padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.time_elapsed_var).grid(row=0, column=2, padx=(0, 20))
        
        # Data Display
        data_frame = ttk.LabelFrame(main_frame, text="Scraped Data", padding="10")
        data_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for data display
        columns = ("Name", "Price", "Rating", "URL")
        self.tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=15)
        
        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Menu Bar
        self.create_menu()
        
        # Status bar
        self.statusbar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initial log message
        self.log_message("Web Scraping Tool initialized successfully!")
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Configuration", command=self.load_config)
        file_menu.add_command(label="Save Configuration", command=self.save_config)
        file_menu.add_separator()
        file_menu.add_command(label="Export CSV", command=lambda: self.export_data("csv"))
        file_menu.add_command(label="Export JSON", command=lambda: self.export_data("json"))
        file_menu.add_command(label="Export Excel", command=lambda: self.export_data("excel"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Check Robots.txt", command=self.check_robots_txt)
        tools_menu.add_command(label="Test URL", command=self.test_url)
        tools_menu.add_command(label="View Source", command=self.view_source)
        tools_menu.add_command(label="Clear Log", command=self.clear_log)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def start_scraping(self):
        """Start the scraping process"""
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Please enter a URL to scrape")
            return
            
        if self.scraping_active:
            messagebox.showwarning("Warning", "Scraping is already in progress")
            return
        
        # Reset data
        self.scraped_data = []
        self.clear_tree()
        
        # Start scraping in background thread
        self.scraping_active = True
        self.stop_scraping = False
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        threading.Thread(target=self.scrape_website, daemon=True).start()
        
    def stop_scraping_process(self):
        """Stop the scraping process"""
        self.stop_scraping = True
        self.log_message("Stopping scraping process...")
        
    def scrape_website(self):
        """Main scraping function"""
        try:
            url = self.url_var.get().strip()
            website_type = self.website_type_var.get()
            max_pages = int(self.max_pages_var.get())
            delay = float(self.delay_var.get())
            
            self.log_message(f"Starting scraping: {url}")
            self.log_message(f"Website type: {website_type}, Max pages: {max_pages}")
            
            start_time = time.time()
            pages_scraped = 0
            items_scraped = 0
            
            # Scrape pages
            for page in range(1, max_pages + 1):
                if self.stop_scraping:
                    break
                    
                # Construct page URL
                if website_type == "books":
                    page_url = f"{url}catalogue/page-{page}.html" if page > 1 else url
                elif website_type == "quotes":
                    page_url = f"{url}page/{page}/" if page > 1 else url
                else:
                    page_url = f"{url}?page={page}" if page > 1 else url
                
                self.status_var.set(f"Scraping page {page}/{max_pages}")
                self.log_message(f"Scraping page {page}: {page_url}")
                
                # Scrape page
                page_items = self.scrape_page(page_url, website_type)
                
                if page_items:
                    self.scraped_data.extend(page_items)
                    items_scraped += len(page_items)
                    pages_scraped += 1
                    
                    # Update UI
                    self.root.after(0, self.update_tree, page_items)
                    self.root.after(0, self.update_stats, items_scraped, pages_scraped, start_time)
                    
                    self.log_message(f"Found {len(page_items)} items on page {page}")
                else:
                    self.log_message(f"No items found on page {page}")
                    if page > 1:  # Stop if no items found on subsequent pages
                        break
                
                # Update progress
                progress = (page / max_pages) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                
                # Delay between requests
                if delay > 0 and page < max_pages:
                    time.sleep(delay)
            
            # Scraping completed
            elapsed_time = time.time() - start_time
            self.log_message(f"Scraping completed! {items_scraped} items from {pages_scraped} pages in {elapsed_time:.2f}s")
            
        except Exception as e:
            self.log_message(f"Error during scraping: {str(e)}")
            messagebox.showerror("Scraping Error", f"An error occurred: {str(e)}")
        
        finally:
            # Reset UI state
            self.root.after(0, self.scraping_finished)
    
    def scrape_page(self, url, website_type):
        """Scrape a single page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            items = []
            
            if website_type == "books":
                items = self.scrape_books_page(soup, url)
            elif website_type == "quotes":
                items = self.scrape_quotes_page(soup, url)
            else:
                items = self.scrape_general_page(soup, url)
            
            return items
            
        except requests.RequestException as e:
            self.log_message(f"Request error for {url}: {str(e)}")
            return []
        except Exception as e:
            self.log_message(f"Parse error for {url}: {str(e)}")
            return []
    
    def scrape_books_page(self, soup, base_url):
        """Scrape books from books.toscrape.com"""
        items = []
        
        book_containers = soup.find_all('article', class_='product_pod')
        
        for book in book_containers:
            try:
                # Extract book information
                title_elem = book.find('h3').find('a')
                title = title_elem.get('title') if title_elem else "N/A"
                
                price_elem = book.find('p', class_='price_color')
                price = price_elem.text.strip() if price_elem else "N/A"
                
                rating_elem = book.find('p', class_='star-rating')
                rating = rating_elem.get('class')[1] if rating_elem else "N/A"
                
                # Convert rating to numeric
                rating_map = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}
                rating = rating_map.get(rating, rating)
                
                link_elem = book.find('h3').find('a')
                relative_url = link_elem.get('href') if link_elem else ""
                full_url = urllib.parse.urljoin(base_url, relative_url)
                
                items.append({
                    'name': title,
                    'price': price,
                    'rating': rating,
                    'url': full_url,
                    'category': 'Book'
                })
                
            except Exception as e:
                self.log_message(f"Error parsing book: {str(e)}")
                continue
        
        return items
    
    def scrape_quotes_page(self, soup, base_url):
        """Scrape quotes from quotes.toscrape.com"""
        items = []
        
        quote_containers = soup.find_all('div', class_='quote')
        
        for quote in quote_containers:
            try:
                text_elem = quote.find('span', class_='text')
                text = text_elem.text.strip() if text_elem else "N/A"
                
                author_elem = quote.find('small', class_='author')
                author = author_elem.text.strip() if author_elem else "N/A"
                
                tags_elems = quote.find_all('a', class_='tag')
                tags = [tag.text.strip() for tag in tags_elems]
                tags_str = ', '.join(tags) if tags else "N/A"
                
                items.append({
                    'name': f"Quote by {author}",
                    'price': text[:50] + "..." if len(text) > 50 else text,
                    'rating': tags_str,
                    'url': base_url,
                    'category': 'Quote'
                })
                
            except Exception as e:
                self.log_message(f"Error parsing quote: {str(e)}")
                continue
        
        return items
    
    def scrape_general_page(self, soup, base_url):
        """General scraping for unknown websites"""
        items = []
        
        # Look for common product containers
        selectors = [
            'div[class*="product"]',
            'div[class*="item"]',
            'article[class*="product"]',
            'li[class*="product"]'
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                break
        
        for container in containers[:20]:  # Limit to first 20 items
            try:
                # Try to find name/title
                name_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.name', '.product-name']
                name = "N/A"
                for sel in name_selectors:
                    elem = container.select_one(sel)
                    if elem:
                        name = elem.get_text(strip=True)
                        break
                
                # Try to find price
                price_selectors = ['.price', '.cost', '[class*="price"]', '[class*="cost"]']
                price = "N/A"
                for sel in price_selectors:
                    elem = container.select_one(sel)
                    if elem:
                        price = elem.get_text(strip=True)
                        break
                
                # Try to find rating
                rating_selectors = ['.rating', '.stars', '[class*="rating"]', '[class*="star"]']
                rating = "N/A"
                for sel in rating_selectors:
                    elem = container.select_one(sel)
                    if elem:
                        rating = elem.get_text(strip=True)
                        break
                
                # Try to find link
                link_elem = container.find('a')
                link = urllib.parse.urljoin(base_url, link_elem.get('href')) if link_elem else base_url
                
                items.append({
                    'name': name,
                    'price': price,
                    'rating': rating,
                    'url': link,
                    'category': 'Product'
                })
                
            except Exception as e:
                self.log_message(f"Error parsing item: {str(e)}")
                continue
        
        return items
    
    def update_tree(self, items):
        """Update the tree view with new items"""
        for item in items:
            self.tree.insert('', 'end', values=(
                item['name'],
                item['price'],
                item['rating'],
                item['url']
            ))
    
    def update_stats(self, items_count, pages_count, start_time):
        """Update statistics display"""
        elapsed_time = time.time() - start_time
        self.items_count_var.set(f"Items: {items_count}")
        self.pages_count_var.set(f"Pages: {pages_count}")
        self.time_elapsed_var.set(f"Time: {elapsed_time:.1f}s")
    
    def scraping_finished(self):
        """Reset UI after scraping is finished"""
        self.scraping_active = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Scraping completed")
        self.progress_var.set(100)
    
    def clear_tree(self):
        """Clear the tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def clear_data(self):
        """Clear all scraped data"""
        self.scraped_data = []
        self.clear_tree()
        self.items_count_var.set("Items: 0")
        self.pages_count_var.set("Pages: 0")
        self.time_elapsed_var.set("Time: 0s")
        self.progress_var.set(0)
        self.log_message("Data cleared")
    
    def export_data(self, format_type=None):
        """Export scraped data to file"""
        if not self.scraped_data:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        if format_type is None:
            format_type = "csv"
        
        # Get filename
        filetypes = {
            "csv": [("CSV files", "*.csv")],
            "json": [("JSON files", "*.json")],
            "excel": [("Excel files", "*.xlsx")]
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=filetypes.get(format_type, [("All files", "*.*")])
        )
        
        if not filename:
            return
        
        try:
            if format_type == "csv":
                self.export_csv(filename)
            elif format_type == "json":
                self.export_json(filename)
            elif format_type == "excel":
                self.export_excel(filename)
            
            self.log_message(f"Data exported to {filename}")
            messagebox.showinfo("Success", f"Data exported successfully to {filename}")
            
        except Exception as e:
            self.log_message(f"Export error: {str(e)}")
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
    
    def export_csv(self, filename):
        """Export data to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'price', 'rating', 'url', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.scraped_data)
    
    def export_json(self, filename):
        """Export data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.scraped_data, jsonfile, indent=2, ensure_ascii=False)
    
    def export_excel(self, filename):
        """Export data to Excel file"""
        df = pd.DataFrame(self.scraped_data)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Scraped Data', index=False)
    
    def check_robots_txt(self):
        """Check robots.txt for the current URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL first")
            return
        
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            can_fetch = rp.can_fetch('*', url)
            
            message = f"Robots.txt URL: {robots_url}\n"
            message += f"Can fetch: {'Yes' if can_fetch else 'No'}\n"
            
            if not can_fetch:
                message += "\n⚠️ Warning: The robots.txt file indicates that this URL should not be scraped."
            
            messagebox.showinfo("Robots.txt Check", message)
            self.log_message(f"Robots.txt check: {robots_url} - Can fetch: {can_fetch}")
            
        except Exception as e:
            self.log_message(f"Robots.txt check error: {str(e)}")
            messagebox.showwarning("Robots.txt Check", f"Could not check robots.txt: {str(e)}")
    
    def test_url(self):
        """Test if URL is accessible"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL first")
            return
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            message = f"URL: {url}\n"
            message += f"Status: {response.status_code}\n"
            message += f"Content-Type: {response.headers.get('content-type', 'Unknown')}\n"
            message += f"Content-Length: {len(response.content)} bytes"
            
            messagebox.showinfo("URL Test", message)
            self.log_message(f"URL test successful: {url}")
            
        except Exception as e:
            self.log_message(f"URL test failed: {str(e)}")
            messagebox.showerror("URL Test", f"Failed to access URL: {str(e)}")
    
    def view_source(self):
        """View page source"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL first")
            return
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Create new window for source view
            source_window = tk.Toplevel(self.root)
            source_window.title(f"Page Source - {url}")
            source_window.geometry("800x600")
            
            text_widget = scrolledtext.ScrolledText(source_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget.insert(tk.END, response.text)
            text_widget.config(state=tk.DISABLED)
            
            self.log_message(f"Page source viewed: {url}")
            
        except Exception as e:
            self.log_message(f"View source error: {str(e)}")
            messagebox.showerror("View Source", f"Failed to get page source: {str(e)}")
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")
    
    def load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            
            self.url_var.set(config.get('url', ''))
            self.website_type_var.set(config.get('website_type', 'books'))
            self.max_pages_var.set(str(config.get('max_pages', 5)))
            self.delay_var.set(str(config.get('delay', 1.0)))
            
            self.log_message(f"Configuration loaded from {filename}")
            
        except Exception as e:
            self.log_message(f"Load config error: {str(e)}")
            messagebox.showerror("Load Configuration", f"Failed to load configuration: {str(e)}")
    
    def save_config(self):
        """Save configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            config = {
                'url': self.url_var.get(),
                'website_type': self.website_type_var.get(),
                'max_pages': int(self.max_pages_var.get()),
                'delay': float(self.delay_var.get())
            }
            
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log_message(f"Configuration saved to {filename}")
            
        except Exception as e:
            self.log_message(f"Save config error: {str(e)}")
            messagebox.showerror("Save Configuration", f"Failed to save configuration: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Web Scraping Tool v1.0

A comprehensive web scraping tool for extracting product information from e-commerce websites.

Features:
• Multiple website support (Books, Quotes, General)
• CSV, JSON, and Excel export
• Robots.txt compliance checking
• Multi-threaded scraping
• Progress tracking
• Configuration save/load

Created for PRODIGY InfoTech Internship - Task 5
        """
        messagebox.showinfo("About", about_text)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
