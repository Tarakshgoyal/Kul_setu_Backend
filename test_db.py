#!/usr/bin/env python3
"""
Test script to verify external database connection
"""
import psycopg2
from psycopg2 import sql

# Database connection parameters
DATABASE_URL = "postgresql://kul_setu_db_user:5xvepfwEtYa0Bzx89vyTiTnUqkJWG437@dpg-d3kjv2ffte5s738ehdh0-a.oregon-postgres.render.com/kul_setu_db"

def test_connection():
    """Test database connection and basic operations"""
    try:
        print("Testing database connection...")
        
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("✅ Successfully connected to external database!")
        
        # Test basic query
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"PostgreSQL version: {version}")
        
        # Check if family_members table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'family_members'
            );
        """)
        
        table_exists = cur.fetchone()[0]
        print(f"family_members table exists: {table_exists}")
        
        if table_exists:
            # Count records in table
            cur.execute("SELECT COUNT(*) FROM family_members;")
            count = cur.fetchone()[0]
            print(f"Records in family_members table: {count}")
        
        cur.close()
        conn.close()
        print("✅ Database test completed successfully!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_connection()