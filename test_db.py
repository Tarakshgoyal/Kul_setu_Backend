import psycopg2

# Test different connection parameters
configs = [
    {"host": "127.0.0.1", "port": "5434", "user": "postgres", "database": "postgres"},
    {"host": "127.0.0.1", "port": "5434", "user": "postgres", "password": "password", "database": "postgres"},
    {"host": "localhost", "port": "5434", "user": "postgres", "database": "postgres"},
    {"host": "localhost", "port": "5434", "user": "postgres", "password": "password", "database": "postgres"},
]

for i, config in enumerate(configs):
    try:
        print(f"Testing config {i+1}: {config}")
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print(f"Success: {result}")
        cur.close()
        conn.close()
        print(f"Working config: {config}")
        break
    except Exception as e:
        print(f"Failed: {e}")
        continue
else:
    print("All configurations failed")