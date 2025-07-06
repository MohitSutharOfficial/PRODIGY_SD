#!/usr/bin/env python3
"""
Data Analysis Script for Web Scraped Data
This script demonstrates how to analyze and work with the scraped CSV data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

def load_and_analyze_data():
    """Load and perform basic analysis on the scraped data"""
    print("🔍 Loading and Analyzing Scraped Data")
    print("=" * 50)
    
    try:
        # Load the CSV data
        df = pd.read_csv('sample_scraped_data.csv')
        
        print(f"📊 Dataset Info:")
        print(f"   • Total records: {len(df)}")
        print(f"   • Columns: {list(df.columns)}")
        print(f"   • Data types: {df.dtypes.to_dict()}")
        
        return df
    except FileNotFoundError:
        print("❌ Error: sample_scraped_data.csv not found!")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def analyze_prices(df):
    """Analyze price data"""
    print("\n💰 Price Analysis")
    print("=" * 30)
    
    # Clean price data (remove £ symbol and convert to float)
    df['price_numeric'] = df['price'].str.replace('£', '', regex=False).astype(float)
    
    print(f"💵 Price Statistics:")
    print(f"   • Average price: £{df['price_numeric'].mean():.2f}")
    print(f"   • Median price: £{df['price_numeric'].median():.2f}")
    print(f"   • Min price: £{df['price_numeric'].min():.2f}")
    print(f"   • Max price: £{df['price_numeric'].max():.2f}")
    print(f"   • Price range: £{df['price_numeric'].max() - df['price_numeric'].min():.2f}")
    
    # Find expensive vs cheap books
    expensive_books = df[df['price_numeric'] > df['price_numeric'].mean()]
    cheap_books = df[df['price_numeric'] <= df['price_numeric'].mean()]
    
    print(f"\n📈 Price Categories:")
    print(f"   • Above average ({len(expensive_books)} books):")
    for _, book in expensive_books.iterrows():
        print(f"     - {book['title'][:50]}... : {book['price']}")
    
    print(f"\n📉 Below/At average ({len(cheap_books)} books):")
    for _, book in cheap_books.iterrows():
        print(f"     - {book['title'][:50]}... : {book['price']}")

def analyze_ratings(df):
    """Analyze rating data"""
    print("\n⭐ Rating Analysis")
    print("=" * 30)
    
    # Convert rating text to numeric
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map)
    
    rating_counts = df['rating'].value_counts()
    print(f"⭐ Rating Distribution:")
    for rating, count in rating_counts.items():
        stars = '⭐' * rating_map.get(rating, 0)
        print(f"   • {rating} stars {stars}: {count} books")
    
    print(f"\n📊 Rating Statistics:")
    print(f"   • Average rating: {df['rating_numeric'].mean():.1f} stars")
    print(f"   • Most common rating: {df['rating'].mode()[0]} stars")
    
    # Best rated books
    best_rated = df[df['rating_numeric'] == df['rating_numeric'].max()]
    print(f"\n🏆 Highest Rated Books ({df['rating_numeric'].max()} stars):")
    for _, book in best_rated.iterrows():
        print(f"   • {book['title'][:60]}... - {book['price']}")

def analyze_availability(df):
    """Analyze availability data"""
    print("\n📦 Availability Analysis")
    print("=" * 30)
    
    availability_counts = df['availability'].value_counts()
    print(f"📋 Availability Status:")
    for status, count in availability_counts.items():
        print(f"   • {status}: {count} books")

def create_visualizations(df):
    """Create data visualizations"""
    print("\n📊 Creating Visualizations")
    print("=" * 30)
    
    try:
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Web Scraped Data Analysis', fontsize=16, fontweight='bold')
        
        # Price distribution
        axes[0, 0].hist(df['price_numeric'], bins=8, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Price Distribution')
        axes[0, 0].set_xlabel('Price (£)')
        axes[0, 0].set_ylabel('Number of Books')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Rating distribution
        rating_counts = df['rating'].value_counts()
        axes[0, 1].bar(rating_counts.index, rating_counts.values, alpha=0.7, color='lightcoral')
        axes[0, 1].set_title('Rating Distribution')
        axes[0, 1].set_xlabel('Rating')
        axes[0, 1].set_ylabel('Number of Books')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Price vs Rating scatter plot
        colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
        for i, (rating, color) in enumerate(zip(['One', 'Two', 'Three', 'Four', 'Five'], colors)):
            mask = df['rating'] == rating
            if mask.any():
                axes[1, 0].scatter(df[mask]['rating_numeric'], df[mask]['price_numeric'], 
                                 alpha=0.7, label=f'{rating} Star', color=color, s=100)
        
        axes[1, 0].set_title('Price vs Rating')
        axes[1, 0].set_xlabel('Rating (Stars)')
        axes[1, 0].set_ylabel('Price (£)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Top 5 most expensive books
        top_books = df.nlargest(5, 'price_numeric')
        axes[1, 1].barh(range(len(top_books)), top_books['price_numeric'], alpha=0.7, color='gold')
        axes[1, 1].set_yticks(range(len(top_books)))
        axes[1, 1].set_yticklabels([title[:25] + '...' if len(title) > 25 else title 
                                   for title in top_books['title']])
        axes[1, 1].set_title('Top 5 Most Expensive Books')
        axes[1, 1].set_xlabel('Price (£)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('scraped_data_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Visualizations saved as 'scraped_data_analysis.png'")
        
    except ImportError:
        print("⚠️  Matplotlib/Seaborn not available for visualizations")
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")

def export_analysis_report(df):
    """Export detailed analysis report"""
    print("\n📝 Exporting Analysis Report")
    print("=" * 30)
    
    try:
        # Create a comprehensive report
        report = f"""
WEB SCRAPING DATA ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================

DATASET OVERVIEW:
• Total Records: {len(df)}
• Date Range: {df['scraped_at'].min()} to {df['scraped_at'].max()}
• Columns: {', '.join(df.columns)}

PRICE ANALYSIS:
• Average Price: £{df['price_numeric'].mean():.2f}
• Median Price: £{df['price_numeric'].median():.2f}
• Price Range: £{df['price_numeric'].min():.2f} - £{df['price_numeric'].max():.2f}
• Standard Deviation: £{df['price_numeric'].std():.2f}

RATING ANALYSIS:
• Average Rating: {df['rating_numeric'].mean():.1f} stars
• Rating Distribution:
{df['rating'].value_counts().to_string()}

AVAILABILITY:
{df['availability'].value_counts().to_string()}

TOP 5 MOST EXPENSIVE BOOKS:
{df.nlargest(5, 'price_numeric')[['title', 'price', 'rating']].to_string(index=False)}

TOP 5 HIGHEST RATED BOOKS:
{df.nlargest(5, 'rating_numeric')[['title', 'price', 'rating']].to_string(index=False)}
"""
        
        with open('analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ Analysis report saved as 'analysis_report.txt'")
        
        # Also save as Excel for advanced analysis
        with pd.ExcelWriter('scraped_data_analysis.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # Summary statistics
            summary_stats = pd.DataFrame({
                'Price Stats': [df['price_numeric'].mean(), df['price_numeric'].median(), 
                               df['price_numeric'].min(), df['price_numeric'].max()],
                'Rating Stats': [df['rating_numeric'].mean(), df['rating_numeric'].median(),
                               df['rating_numeric'].min(), df['rating_numeric'].max()]
            }, index=['Mean', 'Median', 'Min', 'Max'])
            
            summary_stats.to_excel(writer, sheet_name='Summary Stats')
            
        print("✅ Excel analysis saved as 'scraped_data_analysis.xlsx'")
        
    except Exception as e:
        print(f"❌ Error exporting report: {e}")

def main():
    """Main function to run all analyses"""
    print("🕷️ Web Scraping Data Analysis Tool")
    print("=" * 60)
    
    # Load data
    df = load_and_analyze_data()
    if df is None:
        return
    
    # Perform various analyses
    analyze_prices(df)
    analyze_ratings(df)
    analyze_availability(df)
    
    # Create visualizations
    create_visualizations(df)
    
    # Export comprehensive report
    export_analysis_report(df)
    
    print("\n🎉 Analysis Complete!")
    print("=" * 60)
    print("📁 Files created:")
    print("   • analysis_report.txt - Detailed text report")
    print("   • scraped_data_analysis.xlsx - Excel workbook")
    print("   • scraped_data_analysis.png - Visualization charts")
    print("\n💡 You can now use this data for:")
    print("   • Business intelligence and reporting")
    print("   • Price monitoring and comparison")
    print("   • Market research and analysis")
    print("   • Inventory management insights")

if __name__ == "__main__":
    main()
