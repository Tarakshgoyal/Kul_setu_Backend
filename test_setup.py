#!/usr/bin/env python3
"""
Test script to verify the database setup and CSV loading
"""
import psycopg2
import os
import csv
from datetime import datetime

def test_db_connection():
    """Test PostgreSQL connection"""
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kulsetudb',
            user='postgres',
            port='5434'
        )
        print("✅ Database connection successful!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_csv_file():
    """Check if tree.csv exists and is readable"""
    csv_file = 'tree.csv'
    if not os.path.exists(csv_file):
        print(f"❌ CSV file {csv_file} not found!")
        return False
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            row_count = sum(1 for row in csv_reader)
        print(f"✅ CSV file found with {row_count} data rows")
        return True
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return False

def main():
    print("🔍 Testing Kul Setu Backend Setup...")
    print("=" * 50)
    
    # Test database connection
    db_ok = test_db_connection()
    
    # Test CSV file
    csv_ok = check_csv_file()
    
    print("=" * 50)
    if db_ok and csv_ok:
        print("✅ All tests passed! Ready to run the application.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Test the API endpoints")
    else:
        print("❌ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()