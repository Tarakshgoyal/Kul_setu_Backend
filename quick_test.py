#!/usr/bin/env python3
"""
Quick database connection test
"""
import psycopg2

# Database connection
DATABASE_URL = "postgresql://kul_setu_db_user:5xvepfwEtYa0Bzx89vyTiTnUqkJWG437@dpg-d3kjv2ffte5s738ehdh0-a.oregon-postgres.render.com/kul_setu_db"

def test_connection():
    try:
        print("Testing database connection...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Test basic query
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"✅ Connected! PostgreSQL version: {version}")
        
        # Check tables
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cur.fetchall()
        print(f"Tables in database: {[t[0] for t in tables]}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()