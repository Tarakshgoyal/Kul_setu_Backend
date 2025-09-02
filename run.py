#!/usr/bin/env python3
"""
Kul Setu ML Search Backend Runner
Run this file to start the Flask server with ML-based family search
"""

from app import app, search_engine

if __name__ == '__main__':
    print("="*50)
    print("🔍 KUL SETU ML SEARCH BACKEND")
    print("="*50)
    print(f"📊 Loaded {len(search_engine.family_members)} family members")
    print(f"👨‍👩‍👧‍👦 Loaded {len(search_engine.family_map)} families")
    print("🤖 ML Features: TF-IDF + Cosine Similarity")
    print("🔗 Cross-family search enabled")
    print("="*50)
    print("🚀 Starting server at http://127.0.0.1:5000")
    print("📡 CORS enabled for frontend integration")
    print("="*50)
    
    # Test search functionality
    print("\n🧪 Testing search functionality...")
    test_query = {"firstName": "Raj"}
    results = search_engine.search(test_query)
    print(f"✅ Test search for 'Raj': Found {len(results)} results")
    
    app.run(debug=True, host='127.0.0.1', port=5000)