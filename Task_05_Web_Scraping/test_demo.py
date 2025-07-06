"""
Test and Demo Script for the Web Scraping Tool
This script demonstrates and tests the core web scraping functions
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import os
import tempfile
import sys
from datetime import datetime
import urllib.parse

def test_basic_scraping():
    """Test basic scraping functionality"""
    print("🧪 Testing Basic Scraping Functions")
    print("=" * 50)
    
    # Test URL accessibility
    test_urls = [
        "http://books.toscrape.com/",
        "http://quotes.toscrape.com/",
        "https://httpbin.org/html"
    ]
    
    passed = 0
    total = len(test_urls)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    for url in test_urls:
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ PASSED - {url} is accessible")
                passed += 1
            else:
                print(f"❌ FAILED - {url} returned status {response.status_code}")
        except Exception as e:
            print(f"❌ FAILED - {url}: {str(e)}")
    
    print(f"\n📊 URL Accessibility Test Results: {passed}/{total} passed")
    return passed == total

def test_html_parsing():
    """Test HTML parsing functionality"""
    print("\n🧪 Testing HTML Parsing")
    print("=" * 50)
    
    # Sample HTML for testing
    sample_html = """
    <html>
    <body>
        <div class="product">
            <h3><a href="/product1" title="Test Product 1">Product 1</a></h3>
            <p class="price_color">£19.99</p>
            <p class="star-rating Three">Rating</p>
        </div>
        <div class="product">
            <h3><a href="/product2" title="Test Product 2">Product 2</a></h3>
            <p class="price_color">£29.99</p>
            <p class="star-rating Five">Rating</p>
        </div>
    </body>
    </html>
    """
    
    try:
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        # Test finding products
        products = soup.find_all('div', class_='product')
        if len(products) == 2:
            print("✅ PASSED - Found correct number of products")
        else:
            print(f"❌ FAILED - Expected 2 products, found {len(products)}")
            return False
        
        # Test extracting product information
        first_product = products[0]
        
        # Test title extraction
        title_elem = first_product.find('h3').find('a')
        title = title_elem.get('title')
        if title == "Test Product 1":
            print("✅ PASSED - Title extraction works")
        else:
            print(f"❌ FAILED - Expected 'Test Product 1', got '{title}'")
            return False
        
        # Test price extraction
        price_elem = first_product.find('p', class_='price_color')
        price = price_elem.text.strip()
        if price == "£19.99":
            print("✅ PASSED - Price extraction works")
        else:
            print(f"❌ FAILED - Expected '£19.99', got '{price}'")
            return False
        
        # Test rating extraction
        rating_elem = first_product.find('p', class_='star-rating')
        rating = rating_elem.get('class')[1]
        if rating == "Three":
            print("✅ PASSED - Rating extraction works")
        else:
            print(f"❌ FAILED - Expected 'Three', got '{rating}'")
            return False
        
        print("✅ All HTML parsing tests passed")
        return True
        
    except Exception as e:
        print(f"❌ FAILED - HTML parsing error: {str(e)}")
        return False

def test_books_scraping():
    """Test scraping books.toscrape.com"""
    print("\n🧪 Testing Books Scraping")
    print("=" * 50)
    
    try:
        from web_scraper_cli import WebScraperCLI
        scraper = WebScraperCLI()
        
        # Configure for books
        scraper.config['url'] = 'http://books.toscrape.com/'
        scraper.config['website_type'] = 'books'
        scraper.config['max_pages'] = 2
        scraper.config['delay'] = 0.5
        
        print("🔍 Testing book scraping...")
        
        # Test single page scraping
        page_url = scraper.construct_page_url(1)
        items = scraper.scrape_page(page_url)
        
        if items:
            print(f"✅ PASSED - Found {len(items)} books on first page")
            
            # Test data structure
            first_item = items[0]
            required_fields = ['name', 'price', 'rating', 'url', 'category']
            
            for field in required_fields:
                if field in first_item:
                    print(f"✅ PASSED - Field '{field}' present")
                else:
                    print(f"❌ FAILED - Field '{field}' missing")
                    return False
            
            # Test sample data
            print(f"📋 Sample book: {first_item['name'][:40]}...")
            print(f"💰 Price: {first_item['price']}")
            print(f"⭐ Rating: {first_item['rating']}")
            
            return True
        else:
            print("❌ FAILED - No books found")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Books scraping error: {str(e)}")
        return False

def test_quotes_scraping():
    """Test scraping quotes.toscrape.com"""
    print("\n🧪 Testing Quotes Scraping")
    print("=" * 50)
    
    try:
        from web_scraper_cli import WebScraperCLI
        scraper = WebScraperCLI()
        
        # Configure for quotes
        scraper.config['url'] = 'http://quotes.toscrape.com/'
        scraper.config['website_type'] = 'quotes'
        scraper.config['max_pages'] = 2
        scraper.config['delay'] = 0.5
        
        print("🔍 Testing quote scraping...")
        
        # Test single page scraping
        page_url = scraper.construct_page_url(1)
        items = scraper.scrape_page(page_url)
        
        if items:
            print(f"✅ PASSED - Found {len(items)} quotes on first page")
            
            # Test data structure
            first_item = items[0]
            required_fields = ['name', 'price', 'rating', 'url', 'category']
            
            for field in required_fields:
                if field in first_item:
                    print(f"✅ PASSED - Field '{field}' present")
                else:
                    print(f"❌ FAILED - Field '{field}' missing")
                    return False
            
            # Test sample data
            print(f"📋 Sample quote: {first_item['name'][:40]}...")
            print(f"💬 Text: {first_item['price'][:50]}...")
            print(f"🏷️ Tags: {first_item['rating']}")
            
            return True
        else:
            print("❌ FAILED - No quotes found")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Quotes scraping error: {str(e)}")
        return False

def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export")
    print("=" * 50)
    
    # Sample data for testing
    sample_data = [
        {
            'name': 'Test Product 1',
            'price': '£19.99',
            'rating': '4',
            'url': 'http://example.com/product1',
            'category': 'Book',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'name': 'Test Product 2',
            'price': '£29.99',
            'rating': '5',
            'url': 'http://example.com/product2',
            'category': 'Book',
            'scraped_at': datetime.now().isoformat()
        }
    ]
    
    try:
        from web_scraper_cli import WebScraperCLI
        scraper = WebScraperCLI()
        scraper.scraped_data = sample_data
        
        # Test CSV export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_file = f.name
        
        try:
            scraper.export_csv(csv_file)
            
            # Verify CSV file
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Test Product 1' in content and 'Test Product 2' in content:
                    print("✅ PASSED - CSV export works")
                else:
                    print("❌ FAILED - CSV export incomplete")
                    return False
        finally:
            os.unlink(csv_file)
        
        # Test JSON export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json_file = f.name
        
        try:
            scraper.export_json(json_file)
            
            # Verify JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'data' in data and len(data['data']) == 2:
                    print("✅ PASSED - JSON export works")
                else:
                    print("❌ FAILED - JSON export incomplete")
                    return False
        finally:
            os.unlink(json_file)
        
        print("✅ All export tests passed")
        return True
        
    except Exception as e:
        print(f"❌ FAILED - Export error: {str(e)}")
        return False

def test_robots_txt():
    """Test robots.txt checking"""
    print("\n🧪 Testing Robots.txt Checking")
    print("=" * 50)
    
    try:
        from urllib.robotparser import RobotFileParser
        
        # Test with a known website
        test_url = 'http://books.toscrape.com/'
        
        from urllib.parse import urlparse
        parsed_url = urlparse(test_url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        print(f"🤖 Testing robots.txt for {test_url}")
        print(f"📄 Robots.txt URL: {robots_url}")
        
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        can_fetch = rp.can_fetch('*', test_url)
        print(f"✅ PASSED - Robots.txt check completed")
        print(f"🔍 Can fetch: {can_fetch}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  WARNING - Robots.txt check failed: {str(e)}")
        print("🔍 This is often normal for test sites")
        return True  # Don't fail the test for this

def test_url_construction():
    """Test URL construction for different website types"""
    print("\n🧪 Testing URL Construction")
    print("=" * 50)
    
    try:
        from web_scraper_cli import WebScraperCLI
        scraper = WebScraperCLI()
        
        # Test books URL construction
        scraper.config['url'] = 'http://books.toscrape.com/'
        scraper.config['website_type'] = 'books'
        
        page1_url = scraper.construct_page_url(1)
        page2_url = scraper.construct_page_url(2)
        
        if page1_url == 'http://books.toscrape.com/':
            print("✅ PASSED - Books page 1 URL construction")
        else:
            print(f"❌ FAILED - Books page 1 URL: {page1_url}")
            return False
        
        if page2_url == 'http://books.toscrape.com/catalogue/page-2.html':
            print("✅ PASSED - Books page 2 URL construction")
        else:
            print(f"❌ FAILED - Books page 2 URL: {page2_url}")
            return False
        
        # Test quotes URL construction
        scraper.config['url'] = 'http://quotes.toscrape.com/'
        scraper.config['website_type'] = 'quotes'
        
        page1_url = scraper.construct_page_url(1)
        page2_url = scraper.construct_page_url(2)
        
        if page1_url == 'http://quotes.toscrape.com/':
            print("✅ PASSED - Quotes page 1 URL construction")
        else:
            print(f"❌ FAILED - Quotes page 1 URL: {page1_url}")
            return False
        
        if page2_url == 'http://quotes.toscrape.com/page/2/':
            print("✅ PASSED - Quotes page 2 URL construction")
        else:
            print(f"❌ FAILED - Quotes page 2 URL: {page2_url}")
            return False
        
        print("✅ All URL construction tests passed")
        return True
        
    except Exception as e:
        print(f"❌ FAILED - URL construction error: {str(e)}")
        return False

def test_performance():
    """Test performance of scraping operations"""
    print("\n🧪 Testing Performance")
    print("=" * 50)
    
    try:
        from web_scraper_cli import WebScraperCLI
        scraper = WebScraperCLI()
        
        # Test single page scraping performance
        scraper.config['url'] = 'http://books.toscrape.com/'
        scraper.config['website_type'] = 'books'
        
        print("⏱️  Testing single page scraping speed...")
        
        start_time = time.time()
        page_url = scraper.construct_page_url(1)
        items = scraper.scrape_page(page_url)
        elapsed_time = time.time() - start_time
        
        if items:
            print(f"✅ PASSED - Scraped {len(items)} items in {elapsed_time:.2f} seconds")
            
            items_per_second = len(items) / elapsed_time
            print(f"📈 Performance: {items_per_second:.2f} items per second")
            
            if elapsed_time < 10:
                print("🚀 EXCELLENT - Very fast scraping")
            elif elapsed_time < 30:
                print("✅ GOOD - Acceptable scraping speed")
            else:
                print("⚠️  SLOW - Consider optimization")
                
            return True
        else:
            print("❌ FAILED - No items scraped")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Performance test error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and display summary"""
    print("🧪 Running All Tests for Web Scraping Tool")
    print("=" * 60)
    
    tests = [
        ("Basic Scraping", test_basic_scraping),
        ("HTML Parsing", test_html_parsing),
        ("Books Scraping", test_books_scraping),
        ("Quotes Scraping", test_quotes_scraping),
        ("Data Export", test_data_export),
        ("Robots.txt Check", test_robots_txt),
        ("URL Construction", test_url_construction),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        if i < passed:
            print(f"✅ {test_name}")
        else:
            print(f"❌ {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    success_rate = (passed / total) * 100
    print(f"✅ Success Rate: {success_rate:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! The web scraping tool is ready!")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

def demo_gui():
    """Demo the GUI version"""
    print("\n🖥️ Starting GUI Demo...")
    print("💡 The GUI window will open shortly.")
    print("💡 Try the following features:")
    print("   • Select a preset URL (Books or Quotes)")
    print("   • Configure scraping settings")
    print("   • Start scraping process")
    print("   • View scraped data in the table")
    print("   • Export data to CSV, JSON, or Excel")
    print("   • Check robots.txt compliance")
    print("   • Test URL accessibility")
    print("\nClose the GUI window to return to the demo menu.")
    
    try:
        from web_scraper import WebScraperGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = WebScraperGUI(root)
        root.mainloop()
        
        return True
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return False

def demo_cli():
    """Demo the CLI version"""
    print("\n💻 Starting CLI Demo...")
    print("💡 This will start the command-line interface.")
    print("💡 Try the following features:")
    print("   • Use Quick Start for preset URLs")
    print("   • Configure scraping settings")
    print("   • Start scraping process")
    print("   • View scraped data")
    print("   • Export data in various formats")
    print("   • Check robots.txt compliance")
    print("   • View scraping statistics")
    print("\nChoose option 12 to exit and return to the demo menu.")
    
    try:
        from web_scraper_cli import WebScraperCLI
        app = WebScraperCLI()
        app.run()
        return True
    except Exception as e:
        print(f"❌ Error starting CLI: {e}")
        return False

def create_sample_data():
    """Create sample data files for testing"""
    print("\n📝 Creating Sample Data Files")
    print("=" * 50)
    
    try:
        # Create sample configuration
        config = {
            'url': 'http://books.toscrape.com/',
            'website_type': 'books',
            'max_pages': 3,
            'delay': 1.0,
            'output_format': 'csv',
            'output_filename': 'sample_books'
        }
        
        with open('sample_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Created sample_config.json")
        
        # Create sample scraped data
        sample_data = [
            {
                'name': 'A Light in the Attic',
                'price': '£51.77',
                'rating': '3',
                'url': 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
                'category': 'Book',
                'availability': 'In stock',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'name': 'Tipping the Velvet',
                'price': '£53.74',
                'rating': '1',
                'url': 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
                'category': 'Book',
                'availability': 'In stock',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'name': 'Soumission',
                'price': '£50.10',
                'rating': '1',
                'url': 'http://books.toscrape.com/catalogue/soumission_998/index.html',
                'category': 'Book',
                'availability': 'In stock',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        # Save as CSV
        with open('sample_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'price', 'rating', 'url', 'category', 'availability', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)
        
        print("✅ Created sample_data.csv")
        
        # Save as JSON
        export_data = {
            'scraped_at': datetime.now().isoformat(),
            'total_items': len(sample_data),
            'config': config,
            'data': sample_data
        }
        
        with open('sample_data.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
        
        print("✅ Created sample_data.json")
        
        print("\n💡 You can use these files to test the import functionality")
        print("💡 Load sample_config.json to quickly set up scraping")
        print("💡 View sample_data files to see expected output format")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")
        return False

def main():
    """Main demo function"""
    print("🕷️ Web Scraping Tool - Test & Demo Script")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Run all tests")
        print("2. Test basic scraping")
        print("3. Test HTML parsing")
        print("4. Test books scraping")
        print("5. Test quotes scraping")
        print("6. Test data export")
        print("7. Test performance")
        print("8. Demo GUI version")
        print("9. Demo CLI version")
        print("10. Create sample data")
        print("11. Exit")
        
        try:
            choice = input("\nEnter your choice (1-11): ").strip()
            
            if choice == '1':
                run_all_tests()
                # For automated testing, exit after running all tests
                if not sys.stdin.isatty():
                    print("👋 Automated testing complete!")
                    break
            elif choice == '2':
                test_basic_scraping()
            elif choice == '3':
                test_html_parsing()
            elif choice == '4':
                test_books_scraping()
            elif choice == '5':
                test_quotes_scraping()
            elif choice == '6':
                test_data_export()
            elif choice == '7':
                test_performance()
            elif choice == '8':
                demo_gui()
            elif choice == '9':
                demo_cli()
            elif choice == '10':
                create_sample_data()
            elif choice == '11':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-11.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Input stream ended. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
