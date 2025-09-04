#!/usr/bin/env python3
"""
Kul Setu Registration Backend with PostgreSQL
Run this to start the registration service
"""

from app1 import app, init_db
import os

if __name__ == '__main__':
    print("="*50)
    print("📝 KUL SETU REGISTRATION BACKEND")
    print("="*50)
    print("🐘 PostgreSQL Database Integration")
    print("🔗 Cross-Origin Resource Sharing Enabled")
    print("📊 Auto-generates Person/Family IDs")
    print("="*50)
    
    # Initialize database
    print("🔧 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        exit(1)
    
    print("🚀 Starting registration server at http://127.0.0.1:5001")
    print("📡 Endpoints:")
    print("  POST /register - Register new family member")
    print("  GET /members - Get all registered members")
    print("="*50)
    
    app.run(debug=True, host='127.0.0.1', port=5001)