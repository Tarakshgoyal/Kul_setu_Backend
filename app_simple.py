#!/usr/bin/env python3
"""
Simple Flask app startup without CSV loading
"""
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = "postgresql://kul_setu_db_user:5xvepfwEtYa0Bzx89vyTiTnUqkJWG437@dpg-d3kjv2ffte5s738ehdh0-a.oregon-postgres.render.com/kul_setu_db"

def get_db_connection():
    """Get database connection with timeout"""
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=10)
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

@app.route('/')
def home():
    return jsonify({"message": "Kul Setu Backend is running!", "status": "success"})

@app.route('/health')
def health_check():
    try:
        # Test database connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "message": "All systems operational"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get database info
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        
        # Check tables
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "postgresql_version": version,
            "tables": tables
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Kul Setu Backend (Minimal Version)...")
    print("Testing database connection...")
    
    try:
        conn = get_db_connection()
        print("✅ Database connection successful!")
        conn.close()
        
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Failed to start: {e}")