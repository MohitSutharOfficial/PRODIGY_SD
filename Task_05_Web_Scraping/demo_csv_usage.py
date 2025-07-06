#!/usr/bin/env python3
"""
Simple CSV Data Usage Examples
This script shows practical ways to use the scraped CSV data
"""

import pandas as pd
import json

def demo_csv_usage():
    """Demonstrate different ways to use the CSV data"""
    print("📊 CSV Data Usage Examples")
    print("=" * 50)
    
    # Load the data
    df = pd.read_csv('sample_scraped_data.csv')
    
    print("1. 🔍 Basic Data Exploration:")
    print(f"   • Shape: {df.shape}")
    print(f"   • Memory usage: {df.memory_usage().sum()} bytes")
    print(f"   • First book: {df.iloc[0]['title']}")
    print(f"   • Last book: {df.iloc[-1]['title']}")
    
    print("\n2. 💰 Price Analysis:")
    # Convert price to numeric
    df['price_numeric'] = df['price'].str.replace('£', '').astype(float)
    
    print(f"   • Cheapest book: {df.loc[df['price_numeric'].idxmin(), 'title'][:50]}... (£{df['price_numeric'].min():.2f})")
    print(f"   • Most expensive: {df.loc[df['price_numeric'].idxmax(), 'title'][:50]}... (£{df['price_numeric'].max():.2f})")
    
    print("\n3. ⭐ Rating Filter:")
    # Find highly rated books
    high_rated = df[df['rating'].isin(['Four', 'Five'])]
    print(f"   • Books with 4+ stars: {len(high_rated)}")
    for _, book in high_rated.iterrows():
        print(f"     - {book['title'][:40]}... ({book['rating']} stars, {book['price']})")
    
    print("\n4. 📈 Business Intelligence:")
    # Calculate some KPIs
    total_value = df['price_numeric'].sum()
    avg_rating = df['rating'].map({'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}).mean()
    
    print(f"   • Total catalog value: £{total_value:.2f}")
    print(f"   • Average rating: {avg_rating:.1f} stars")
    print(f"   • Books above average price: {len(df[df['price_numeric'] > df['price_numeric'].mean()])}")
    
    print("\n5. 📱 Export for Other Applications:")
    
    # Export subset of data
    export_data = df[['title', 'price', 'rating', 'availability']].head(3)
    
    # As JSON for APIs
    json_data = export_data.to_json(orient='records', indent=2)
    print("   • JSON format (first 3 records):")
    print(json_data[:200] + "...")
    
    # As HTML table for web
    html_table = export_data.to_html(index=False, classes='table table-striped')
    print(f"\n   • HTML table length: {len(html_table)} characters")
    
    # As dictionary for Python processing
    dict_data = export_data.to_dict('records')
    print(f"   • Dictionary format: {len(dict_data)} records")
    
    print("\n6. 🔄 Data Transformation:")
    # Create new columns
    df['price_category'] = df['price_numeric'].apply(
        lambda x: 'Expensive' if x > 40 else 'Moderate' if x > 25 else 'Cheap'
    )
    
    category_counts = df['price_category'].value_counts()
    print("   • Price categories:")
    for category, count in category_counts.items():
        print(f"     - {category}: {count} books")
    
    print("\n7. 🎯 Practical Applications:")
    print("   • E-commerce price monitoring")
    print("   • Market research and competitor analysis")
    print("   • Inventory management and stock tracking")
    print("   • Customer recommendation systems")
    print("   • Business reporting and analytics")
    print("   • Data science and machine learning projects")
    
    return df

if __name__ == "__main__":
    demo_csv_usage()
