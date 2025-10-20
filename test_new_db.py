import psycopg2
import os

print("=== Testing New Database Connection ===")

# New database URL
new_db_url = "postgresql://kul_setu_db_u64s_user:QNIomHFakekLB4I2nKPmPAMDAfkMR2jp@dpg-d3muriidbo4c73asequg-a.oregon-postgres.render.com/kul_setu_db_u64s"

try:
    print("Attempting to connect to new database...")
    conn = psycopg2.connect(new_db_url)
    print("✅ Connection successful!")
    
    # Test basic query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0][:50]}...")
    
    # Check if any tables exist
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    print(f"\nExisting tables: {len(tables)}")
    if tables:
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("  No tables found (fresh database)")
    
    cur.close()
    conn.close()
    print("\n✅ Database is ready to use!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
