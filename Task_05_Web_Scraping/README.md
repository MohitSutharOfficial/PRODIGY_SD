# Web Scraping Tool

A comprehensive web scraping tool for extracting product information from e-commerce websites with both GUI and CLI interfaces, featuring ethical scraping practices and multiple export formats.

## Features

### Core Functionality
- **Multi-Website Support**: Specialized scrapers for books, quotes, and general e-commerce sites
- **Dual Interface**: Both GUI and command-line interfaces available
- **Ethical Scraping**: Robots.txt compliance checking and request delays
- **Data Export**: Multiple formats (CSV, JSON, Excel) with comprehensive data
- **Real-time Progress**: Live progress tracking and status updates
- **Error Handling**: Robust error management and recovery

### Advanced Features
- **Session Management**: Persistent HTTP sessions for better performance
- **User-Agent Rotation**: Professional browser user-agent strings
- **Configurable Delays**: Customizable delays between requests
- **Batch Processing**: Multi-page scraping with pagination support
- **Data Validation**: Automatic data cleaning and validation
- **Statistics**: Detailed scraping statistics and performance metrics

### Supported Websites
- **Books to Scrape**: http://books.toscrape.com/ (Books catalog)
- **Quotes to Scrape**: http://quotes.toscrape.com/ (Famous quotes)
- **General E-commerce**: Adaptive scraping for various product sites
- **Custom Sites**: Configurable selectors for new websites

### Data Extraction
- **Product Names**: Titles, descriptions, and identifiers
- **Pricing Information**: Current prices, discounts, and currency
- **Ratings & Reviews**: Star ratings and review counts
- **Availability**: Stock status and availability information
- **Metadata**: URLs, categories, and timestamps

## Files

- `web_scraper.py` - GUI version with tkinter interface
- `web_scraper_cli.py` - Command-line interface version
- `test_demo.py` - Comprehensive testing and demonstration script
- `run_scraper.bat` - Windows batch launcher
- `requirements.txt` - Project dependencies
- `README.md` - This documentation file

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection for scraping

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
```bash
pip install requests beautifulsoup4 pandas openpyxl lxml
```

## Usage

### GUI Version (Recommended)
```bash
python web_scraper.py
```

### CLI Version
```bash
python web_scraper_cli.py
```

### Using the Batch Launcher (Windows)
```bash
run_scraper.bat
```

### Running Tests and Demos
```bash
python test_demo.py
```

## GUI Interface Guide

### Main Window Features
- **URL Input**: Enter target website URL or select from presets
- **Configuration Panel**: Set website type, max pages, and delays
- **Progress Tracking**: Real-time progress bar and statistics
- **Data Table**: Live display of scraped data with sortable columns
- **Export Options**: Multiple format export with file selection
- **Activity Log**: Detailed logging of all scraping activities

### Control Buttons
- **🚀 Start Scraping**: Begin the scraping process
- **🛑 Stop Scraping**: Safely halt ongoing scraping
- **🗑️ Clear Data**: Remove all scraped data
- **💾 Export Data**: Save data to file
- **🤖 Check Robots.txt**: Verify scraping permissions

### Menu Options
- **File Menu**: Load/save configurations, export data
- **Tools Menu**: URL testing, source viewing, robots.txt checking
- **Help Menu**: About dialog and documentation

## CLI Interface Guide

### Main Menu Options
1. **🚀 Start Scraping**: Begin scraping with current configuration
2. **⚙️ Configure Settings**: Set URL, website type, pages, delays
3. **📊 View Scraped Data**: Display all scraped items
4. **💾 Export Data**: Save to CSV, JSON, or Excel
5. **📋 Load Configuration**: Load settings from file
6. **💾 Save Configuration**: Save current settings
7. **🤖 Check Robots.txt**: Verify scraping permissions
8. **🔍 Test URL**: Check URL accessibility
9. **🌐 Quick Start**: Use preset URLs for common sites
10. **📈 View Statistics**: See scraping analytics
11. **🗑️ Clear Data**: Remove all scraped data
12. **🚪 Exit**: Close the application

### Configuration Options
- **URL**: Target website address
- **Website Type**: books, quotes, or general
- **Max Pages**: Number of pages to scrape
- **Delay**: Seconds between requests
- **Output Format**: CSV, JSON, or Excel
- **Output Filename**: Base name for exported files

## Website Types

### Books (books.toscrape.com)
- **Data Extracted**: Title, price, rating, availability, URL
- **Pagination**: Automatic page navigation
- **Special Features**: Star rating conversion, stock status

### Quotes (quotes.toscrape.com)
- **Data Extracted**: Quote text, author, tags, URL
- **Pagination**: Automatic page navigation
- **Special Features**: Tag collection, author information

### General E-commerce
- **Data Extracted**: Product name, price, rating, URL
- **Adaptive Scraping**: Automatically detects common selectors
- **Flexible Parsing**: Handles various HTML structures

## Data Export Formats

### CSV Export
- **Format**: Comma-separated values
- **Headers**: name, price, rating, url, category, scraped_at
- **Encoding**: UTF-8 with BOM for Excel compatibility
- **Use Case**: Spreadsheet analysis, data import

### JSON Export
- **Format**: JavaScript Object Notation
- **Structure**: Metadata + data array
- **Fields**: All scraped data plus configuration
- **Use Case**: Data processing, API integration

### Excel Export
- **Format**: Microsoft Excel (.xlsx)
- **Sheets**: Data + Summary
- **Features**: Formatted headers, auto-sizing
- **Use Case**: Business reports, data analysis

## Ethical Scraping Practices

### Robots.txt Compliance
- **Automatic Checking**: Built-in robots.txt parser
- **Compliance Warning**: Alerts for restricted URLs
- **Respect Guidelines**: Follows website scraping policies

### Rate Limiting
- **Configurable Delays**: Customizable request intervals
- **Default Delays**: Conservative 1-second default
- **Burst Protection**: Prevents overwhelming servers

### User-Agent Management
- **Professional Headers**: Legitimate browser user-agents
- **Transparent Identification**: Clear tool identification
- **Respectful Requests**: Standard HTTP practices

## Performance Optimization

### Session Management
- **Connection Reuse**: Persistent HTTP sessions
- **Cookie Handling**: Automatic cookie management
- **Header Optimization**: Efficient request headers

### Data Processing
- **Streaming Parsing**: Memory-efficient HTML parsing
- **Batch Processing**: Efficient multi-page handling
- **Error Recovery**: Graceful failure handling

### Memory Management
- **Lazy Loading**: Process data as needed
- **Garbage Collection**: Automatic memory cleanup
- **Resource Monitoring**: Track resource usage

## Error Handling

### Network Errors
- **Timeout Handling**: Configurable request timeouts
- **Connection Retry**: Automatic retry on failures
- **Status Code Handling**: Proper HTTP status processing

### Parsing Errors
- **HTML Validation**: Robust HTML parsing
- **Missing Elements**: Graceful handling of missing data
- **Encoding Issues**: Automatic encoding detection

### Data Validation
- **Field Validation**: Ensure required fields present
- **Type Checking**: Validate data types
- **Sanitization**: Clean and normalize data

## Testing

### Automated Tests
- **Unit Tests**: Individual component testing
- **Integration Tests**: Full workflow testing
- **Performance Tests**: Speed and efficiency validation

### Test Coverage
- **Basic Scraping**: Core functionality verification
- **HTML Parsing**: Parser accuracy testing
- **Data Export**: Format validation
- **Error Handling**: Exception management testing

### Test Data
- **Sample Sites**: Known working test websites
- **Mock Data**: Controlled test scenarios
- **Edge Cases**: Boundary condition testing

## Configuration

### Settings File
```json
{
  "url": "http://books.toscrape.com/",
  "website_type": "books",
  "max_pages": 5,
  "delay": 1.0,
  "output_format": "csv",
  "output_filename": "scraped_data"
}
```

### Environment Variables
- **SCRAPER_DELAY**: Default delay between requests
- **SCRAPER_TIMEOUT**: Request timeout in seconds
- **SCRAPER_MAX_PAGES**: Maximum pages to scrape

## Troubleshooting

### Common Issues
1. **Connection Errors**: Check internet connectivity
2. **Blocked Requests**: Verify robots.txt compliance
3. **Missing Data**: Confirm website structure hasn't changed
4. **Slow Performance**: Increase delay between requests

### Debug Mode
- **Verbose Logging**: Enable detailed logging
- **Source Viewing**: Inspect HTML source
- **Step-by-Step**: Manual page-by-page scraping

### Support Resources
- **Test URLs**: Use provided test websites
- **Sample Data**: Reference example outputs
- **Documentation**: Comprehensive guides

## Best Practices

### Ethical Guidelines
- **Respect robots.txt**: Always check and follow
- **Use delays**: Don't overwhelm servers
- **Identify yourself**: Use appropriate user-agents
- **Limit scope**: Only scrape what you need

### Technical Tips
- **Start small**: Test with few pages first
- **Monitor performance**: Watch for slowdowns
- **Handle errors**: Implement proper error handling
- **Clean data**: Validate and sanitize output

### Legal Considerations
- **Public data only**: Scrape publicly available information
- **Respect terms**: Follow website terms of service
- **Commercial use**: Understand commercial usage rights
- **Attribution**: Credit data sources when required

## Advanced Features

### Custom Selectors
- **CSS Selectors**: Define custom element selectors
- **XPath Support**: Advanced element targeting
- **Dynamic Configuration**: Runtime selector modification

### Batch Operations
- **Multi-site Scraping**: Process multiple websites
- **Scheduled Scraping**: Automated periodic updates
- **Bulk Export**: Mass data export operations

### Integration Options
- **API Endpoints**: RESTful API for automation
- **Database Storage**: Direct database integration
- **Cloud Export**: Cloud storage compatibility

## Development

### Code Structure
- **Modular Design**: Separate components for different functions
- **Object-Oriented**: Clean class-based architecture
- **Documentation**: Comprehensive code comments
- **Testing**: Full test suite coverage

### Extension Points
- **Custom Parsers**: Add support for new websites
- **Export Formats**: Implement additional formats
- **UI Themes**: Customize interface appearance
- **Plugin System**: Extensible architecture

## Security

### Data Protection
- **Local Storage**: All data stored locally
- **No Tracking**: No user activity tracking
- **Secure Requests**: HTTPS support
- **Data Encryption**: Optional data encryption

### Privacy Features
- **Anonymous Scraping**: No personal data collection
- **Temporary Files**: Automatic cleanup
- **Secure Export**: Safe file handling

## License

This project is part of the PRODIGY InfoTech internship program and is intended for educational and professional development purposes.

## Contributing

### Bug Reports
- **Issue Tracking**: Report bugs and issues
- **Feature Requests**: Suggest new features
- **Documentation**: Improve documentation

### Development Guidelines
- **Code Style**: Follow PEP 8 standards
- **Testing**: Include tests for new features
- **Documentation**: Update docs for changes

## Changelog

### Version 1.0.0
- Initial release with GUI and CLI interfaces
- Support for books and quotes scraping
- CSV, JSON, and Excel export formats
- Comprehensive testing suite
- Ethical scraping features

---

**Web Scraping Tool** - Professional, ethical, and efficient web scraping! 🕷️✨
