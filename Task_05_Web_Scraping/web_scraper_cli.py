"""
Web Scraping Tool - Command Line Version
A comprehensive CLI-based web scraping tool for extracting product information from e-commerce websites.
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import time
import os
import re
from datetime import datetime
import urllib.parse
from urllib.robotparser import RobotFileParser

class WebScraperCLI:
    def __init__(self):
        self.scraped_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.config = {
            'url': '',
            'website_type': 'books',
            'max_pages': 5,
            'delay': 1.0,
            'output_format': 'csv',
            'output_filename': 'scraped_data'
        }
        
    def display_header(self):
        """Display application header"""
        print("\n" + "="*60)
        print("🕷️  WEB SCRAPING TOOL - CLI VERSION")
        print("="*60)
        print("Extract product information from e-commerce websites")
        print("Created for PRODIGY InfoTech Internship - Task 5")
        print("="*60)
        
    def display_menu(self):
        """Display main menu"""
        print("\n📋 MAIN MENU")
        print("="*40)
        print("1. 🚀 Start Scraping")
        print("2. ⚙️  Configure Settings")
        print("3. 📊 View Scraped Data")
        print("4. 💾 Export Data")
        print("5. 📋 Load Configuration")
        print("6. 💾 Save Configuration")
        print("7. 🤖 Check Robots.txt")
        print("8. 🔍 Test URL")
        print("9. 🌐 Quick Start (Preset URLs)")
        print("10. 📈 View Statistics")
        print("11. 🗑️  Clear Data")
        print("12. 🚪 Exit")
        print("="*40)
        
    def get_user_choice(self):
        """Get user menu choice"""
        while True:
            try:
                choice = input("\n👉 Enter your choice (1-12): ").strip()
                if choice in [str(i) for i in range(1, 13)]:
                    return int(choice)
                else:
                    print("❌ Invalid choice. Please enter 1-12.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return 12
            except Exception:
                print("❌ Invalid input. Please enter a number.")
                
    def configure_settings(self):
        """Configure scraping settings"""
        print("\n⚙️  CONFIGURATION")
        print("="*40)
        
        print(f"Current URL: {self.config['url']}")
        new_url = input("Enter new URL (or press Enter to keep current): ").strip()
        if new_url:
            self.config['url'] = new_url
            
        print(f"Current website type: {self.config['website_type']}")
        print("Available types: books, quotes, general")
        new_type = input("Enter website type (or press Enter to keep current): ").strip()
        if new_type and new_type in ['books', 'quotes', 'general']:
            self.config['website_type'] = new_type
            
        print(f"Current max pages: {self.config['max_pages']}")
        try:
            new_pages = input("Enter max pages (or press Enter to keep current): ").strip()
            if new_pages:
                self.config['max_pages'] = int(new_pages)
        except ValueError:
            print("❌ Invalid number, keeping current value")
            
        print(f"Current delay: {self.config['delay']} seconds")
        try:
            new_delay = input("Enter delay between requests (or press Enter to keep current): ").strip()
            if new_delay:
                self.config['delay'] = float(new_delay)
        except ValueError:
            print("❌ Invalid number, keeping current value")
            
        print(f"Current output format: {self.config['output_format']}")
        print("Available formats: csv, json, excel")
        new_format = input("Enter output format (or press Enter to keep current): ").strip()
        if new_format and new_format in ['csv', 'json', 'excel']:
            self.config['output_format'] = new_format
            
        print(f"Current output filename: {self.config['output_filename']}")
        new_filename = input("Enter output filename (or press Enter to keep current): ").strip()
        if new_filename:
            self.config['output_filename'] = new_filename
            
        print("✅ Configuration updated successfully!")
        
    def start_scraping(self):
        """Start the web scraping process"""
        if not self.config['url']:
            print("❌ Please configure a URL first!")
            return
            
        print("\n🚀 STARTING WEB SCRAPING")
        print("="*40)
        print(f"URL: {self.config['url']}")
        print(f"Website Type: {self.config['website_type']}")
        print(f"Max Pages: {self.config['max_pages']}")
        print(f"Delay: {self.config['delay']} seconds")
        print("="*40)
        
        # Clear previous data
        self.scraped_data = []
        
        start_time = time.time()
        total_items = 0
        pages_scraped = 0
        
        try:
            for page in range(1, self.config['max_pages'] + 1):
                print(f"\n📄 Scraping page {page}/{self.config['max_pages']}...")
                
                # Construct page URL
                page_url = self.construct_page_url(page)
                print(f"🔗 URL: {page_url}")
                
                # Scrape page
                page_items = self.scrape_page(page_url)
                
                if page_items:
                    self.scraped_data.extend(page_items)
                    total_items += len(page_items)
                    pages_scraped += 1
                    print(f"✅ Found {len(page_items)} items on page {page}")
                    
                    # Display sample items
                    print("📋 Sample items:")
                    for i, item in enumerate(page_items[:3]):
                        print(f"   {i+1}. {item['name'][:50]}...")
                        
                else:
                    print(f"❌ No items found on page {page}")
                    if page > 1:  # Stop if no items found on subsequent pages
                        print("🛑 Stopping - no more items found")
                        break
                
                # Delay between requests
                if self.config['delay'] > 0 and page < self.config['max_pages']:
                    print(f"⏱️  Waiting {self.config['delay']} seconds...")
                    time.sleep(self.config['delay'])
                    
        except KeyboardInterrupt:
            print("\n🛑 Scraping stopped by user")
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            
        # Display results
        elapsed_time = time.time() - start_time
        print(f"\n🎉 SCRAPING COMPLETED!")
        print("="*40)
        print(f"Total items: {total_items}")
        print(f"Pages scraped: {pages_scraped}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        print(f"Average time per page: {elapsed_time/pages_scraped:.2f} seconds" if pages_scraped > 0 else "")
        
        if total_items > 0:
            print(f"✅ Data ready for export!")
        else:
            print("❌ No data scraped")
            
    def construct_page_url(self, page):
        """Construct URL for specific page"""
        url = self.config['url']
        website_type = self.config['website_type']
        
        if website_type == "books":
            return f"{url}catalogue/page-{page}.html" if page > 1 else url
        elif website_type == "quotes":
            return f"{url}page/{page}/" if page > 1 else url
        else:
            return f"{url}?page={page}" if page > 1 else url
            
    def scrape_page(self, url):
        """Scrape a single page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if self.config['website_type'] == "books":
                return self.scrape_books_page(soup, url)
            elif self.config['website_type'] == "quotes":
                return self.scrape_quotes_page(soup, url)
            else:
                return self.scrape_general_page(soup, url)
                
        except requests.RequestException as e:
            print(f"❌ Request error: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Parse error: {str(e)}")
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
                
                availability_elem = book.find('p', class_='instock availability')
                availability = availability_elem.text.strip() if availability_elem else "N/A"
                
                items.append({
                    'name': title,
                    'price': price,
                    'rating': rating,
                    'url': full_url,
                    'category': 'Book',
                    'availability': availability,
                    'scraped_at': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"❌ Error parsing book: {str(e)}")
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
                    'price': text,
                    'rating': tags_str,
                    'url': base_url,
                    'category': 'Quote',
                    'author': author,
                    'text': text,
                    'tags': tags_str,
                    'scraped_at': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"❌ Error parsing quote: {str(e)}")
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
        
        containers = []
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
                    'category': 'Product',
                    'scraped_at': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"❌ Error parsing item: {str(e)}")
                continue
                
        return items
        
    def view_scraped_data(self):
        """Display scraped data"""
        if not self.scraped_data:
            print("❌ No data available. Please scrape some data first.")
            return
            
        print(f"\n📊 SCRAPED DATA ({len(self.scraped_data)} items)")
        print("="*60)
        
        for i, item in enumerate(self.scraped_data, 1):
            print(f"\n📦 Item {i}:")
            print(f"   Name: {item['name']}")
            print(f"   Price: {item['price']}")
            print(f"   Rating: {item['rating']}")
            print(f"   Category: {item['category']}")
            print(f"   URL: {item['url']}")
            
            if i >= 10:  # Limit display to first 10 items
                remaining = len(self.scraped_data) - 10
                if remaining > 0:
                    print(f"\n... and {remaining} more items")
                break
                
        print(f"\n📈 Total items: {len(self.scraped_data)}")
        
    def export_data(self):
        """Export scraped data to file"""
        if not self.scraped_data:
            print("❌ No data to export. Please scrape some data first.")
            return
            
        print(f"\n💾 EXPORT DATA")
        print("="*30)
        print(f"Current format: {self.config['output_format']}")
        print(f"Current filename: {self.config['output_filename']}")
        
        # Ask for confirmation or new settings
        choice = input("\n1. Export with current settings\n2. Change settings\nChoice (1-2): ").strip()
        
        if choice == '2':
            new_format = input("Enter format (csv/json/excel): ").strip()
            if new_format in ['csv', 'json', 'excel']:
                self.config['output_format'] = new_format
                
            new_filename = input("Enter filename (without extension): ").strip()
            if new_filename:
                self.config['output_filename'] = new_filename
                
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.config['output_filename']}_{timestamp}"
            
            if self.config['output_format'] == 'csv':
                filename += '.csv'
                self.export_csv(filename)
            elif self.config['output_format'] == 'json':
                filename += '.json'
                self.export_json(filename)
            elif self.config['output_format'] == 'excel':
                filename += '.xlsx'
                self.export_excel(filename)
                
            print(f"✅ Data exported successfully to {filename}")
            print(f"📁 File location: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"❌ Export error: {str(e)}")
            
    def export_csv(self, filename):
        """Export data to CSV file"""
        fieldnames = ['name', 'price', 'rating', 'url', 'category', 'scraped_at']
        if self.scraped_data and 'author' in self.scraped_data[0]:
            fieldnames.extend(['author', 'text', 'tags'])
        if self.scraped_data and 'availability' in self.scraped_data[0]:
            fieldnames.append('availability')
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(self.scraped_data)
            
    def export_json(self, filename):
        """Export data to JSON file"""
        export_data = {
            'scraped_at': datetime.now().isoformat(),
            'total_items': len(self.scraped_data),
            'config': self.config,
            'data': self.scraped_data
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
            
    def export_excel(self, filename):
        """Export data to Excel file"""
        df = pd.DataFrame(self.scraped_data)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Scraped Data', index=False)
            
            # Add summary sheet
            summary_data = {
                'Total Items': [len(self.scraped_data)],
                'Scraped At': [datetime.now().isoformat()],
                'Website Type': [self.config['website_type']],
                'Source URL': [self.config['url']]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
    def check_robots_txt(self):
        """Check robots.txt for the current URL"""
        if not self.config['url']:
            print("❌ Please configure a URL first!")
            return
            
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(self.config['url'])
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            print(f"\n🤖 ROBOTS.TXT CHECK")
            print("="*30)
            print(f"URL: {self.config['url']}")
            print(f"Robots.txt: {robots_url}")
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            can_fetch = rp.can_fetch('*', self.config['url'])
            
            print(f"Can fetch: {'✅ Yes' if can_fetch else '❌ No'}")
            
            if not can_fetch:
                print("\n⚠️  WARNING: The robots.txt file indicates that this URL should not be scraped.")
                print("Please respect the website's robots.txt policy.")
            else:
                print("\n✅ The URL appears to be allowed for scraping according to robots.txt.")
                
        except Exception as e:
            print(f"❌ Could not check robots.txt: {str(e)}")
            
    def test_url(self):
        """Test if URL is accessible"""
        if not self.config['url']:
            print("❌ Please configure a URL first!")
            return
            
        try:
            print(f"\n🔍 TESTING URL")
            print("="*30)
            print(f"URL: {self.config['url']}")
            
            start_time = time.time()
            response = self.session.get(self.config['url'], timeout=10)
            elapsed_time = time.time() - start_time
            
            response.raise_for_status()
            
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Response time: {elapsed_time:.2f} seconds")
            print(f"✅ Content-Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"✅ Content-Length: {len(response.content)} bytes")
            
            # Check for common anti-scraping measures
            if 'cloudflare' in response.text.lower():
                print("⚠️  Warning: Cloudflare detected - may have anti-scraping measures")
            if 'captcha' in response.text.lower():
                print("⚠️  Warning: CAPTCHA detected - may block automated requests")
                
        except Exception as e:
            print(f"❌ Failed to access URL: {str(e)}")
            
    def quick_start(self):
        """Quick start with preset URLs"""
        print("\n🌐 QUICK START - PRESET URLS")
        print("="*40)
        
        presets = [
            {
                'name': 'Books to Scrape',
                'url': 'http://books.toscrape.com/',
                'type': 'books',
                'description': 'Sample bookstore for testing scrapers'
            },
            {
                'name': 'Quotes to Scrape',
                'url': 'http://quotes.toscrape.com/',
                'type': 'quotes',
                'description': 'Famous quotes collection'
            },
            {
                'name': 'Scrape Me (Pokemon)',
                'url': 'https://scrapeme.live/shop/',
                'type': 'general',
                'description': 'Pokemon product catalog'
            }
        ]
        
        for i, preset in enumerate(presets, 1):
            print(f"{i}. {preset['name']}")
            print(f"   URL: {preset['url']}")
            print(f"   Type: {preset['type']}")
            print(f"   Description: {preset['description']}")
            print()
            
        try:
            choice = input("Choose preset (1-3) or 0 to cancel: ").strip()
            choice = int(choice)
            
            if choice == 0:
                return
            elif 1 <= choice <= len(presets):
                preset = presets[choice - 1]
                self.config['url'] = preset['url']
                self.config['website_type'] = preset['type']
                print(f"✅ Configuration updated to {preset['name']}")
            else:
                print("❌ Invalid choice")
                
        except ValueError:
            print("❌ Invalid input")
            
    def view_statistics(self):
        """View scraping statistics"""
        if not self.scraped_data:
            print("❌ No data available for statistics.")
            return
            
        print(f"\n📈 STATISTICS")
        print("="*40)
        
        total_items = len(self.scraped_data)
        print(f"Total Items: {total_items}")
        
        # Category breakdown
        categories = {}
        for item in self.scraped_data:
            cat = item.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
        print(f"\nCategory Breakdown:")
        for cat, count in categories.items():
            percentage = (count / total_items) * 100
            print(f"  {cat}: {count} ({percentage:.1f}%)")
            
        # Price analysis (if available)
        prices = []
        for item in self.scraped_data:
            price_str = item.get('price', '')
            if price_str and price_str != 'N/A':
                # Extract numeric price
                price_match = re.search(r'[\d.]+', price_str)
                if price_match:
                    try:
                        prices.append(float(price_match.group()))
                    except ValueError:
                        pass
                        
        if prices:
            print(f"\nPrice Analysis:")
            print(f"  Items with prices: {len(prices)}")
            print(f"  Average price: ${sum(prices) / len(prices):.2f}")
            print(f"  Min price: ${min(prices):.2f}")
            print(f"  Max price: ${max(prices):.2f}")
            
    def clear_data(self):
        """Clear all scraped data"""
        if not self.scraped_data:
            print("❌ No data to clear.")
            return
            
        confirm = input(f"Are you sure you want to clear {len(self.scraped_data)} items? (y/N): ").strip().lower()
        if confirm == 'y':
            self.scraped_data = []
            print("✅ Data cleared successfully.")
        else:
            print("❌ Operation cancelled.")
            
    def load_config(self):
        """Load configuration from file"""
        filename = input("Enter configuration filename (or press Enter for 'config.json'): ").strip()
        if not filename:
            filename = 'config.json'
            
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
                
            self.config.update(config)
            print(f"✅ Configuration loaded from {filename}")
            
        except FileNotFoundError:
            print(f"❌ Configuration file {filename} not found.")
        except Exception as e:
            print(f"❌ Error loading configuration: {str(e)}")
            
    def save_config(self):
        """Save configuration to file"""
        filename = input("Enter configuration filename (or press Enter for 'config.json'): ").strip()
        if not filename:
            filename = 'config.json'
            
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=2)
                
            print(f"✅ Configuration saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving configuration: {str(e)}")
            
    def run(self):
        """Run the main application loop"""
        self.display_header()
        
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                
                if choice == 1:
                    self.start_scraping()
                elif choice == 2:
                    self.configure_settings()
                elif choice == 3:
                    self.view_scraped_data()
                elif choice == 4:
                    self.export_data()
                elif choice == 5:
                    self.load_config()
                elif choice == 6:
                    self.save_config()
                elif choice == 7:
                    self.check_robots_txt()
                elif choice == 8:
                    self.test_url()
                elif choice == 9:
                    self.quick_start()
                elif choice == 10:
                    self.view_statistics()
                elif choice == 11:
                    self.clear_data()
                elif choice == 12:
                    print("👋 Thank you for using Web Scraping Tool!")
                    print("💾 All data has been preserved for your next session.")
                    break
                    
                # Pause before showing menu again
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                input("\n⏸️  Press Enter to continue...")

def main():
    """Main function to run the CLI application"""
    try:
        app = WebScraperCLI()
        app.run()
    except Exception as e:
        print(f"❌ Application error: {str(e)}")

if __name__ == "__main__":
    main()
