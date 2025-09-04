from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import re
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid #data.json
import os

app = Flask(__name__)
CORS(app)
def get_db_connection(database="kulsetudb"):
    return psycopg2.connect(
        host='127.0.0.1',
        database=database,
        user='postgres',
        port='5434'
    )
def init_db():
    # First connect to default postgres database
    conn = get_db_connection("postgres")
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create kulsetudb if it doesn't exist
    cur.execute("SELECT 1 FROM pg_database WHERE datname='kulsetudb'")
    if not cur.fetchone():
        cur.execute("CREATE DATABASE kulsetudb")
    
    cur.close()
    conn.close()
    
    # Now connect to kulsetudb and create table
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS family_members (
            person_id VARCHAR(50) PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            family_id VARCHAR(50) NOT NULL,
            father_id VARCHAR(50),
            mother_id VARCHAR(50),
            generation INTEGER NOT NULL,
            birth_year INTEGER NOT NULL,
            blood_group VARCHAR(10) NOT NULL,
            eye_color VARCHAR(20) NOT NULL,
            birthmark TEXT,
            disease TEXT,
            passion VARCHAR(100) NOT NULL,
            trait VARCHAR(100) NOT NULL,
            nature VARCHAR(100) NOT NULL,
            about TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def generate_id():
    return str(uuid.uuid4())[:8].upper()
@app.route('/register', methods=['POST'])
def register_member():
    try:
        data = request.get_json()
        
        # Generate IDs if not provided
        person_id = data.get('personId') or generate_id()
        family_id = data.get('familyId') or generate_id()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO family_members (
                person_id, first_name, last_name, family_id, father_id, mother_id,
                generation, birth_year, blood_group, eye_color, birthmark, disease,
                passion, trait, nature, about
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            person_id,
            data['firstName'],
            data['lastName'],
            family_id,
            data.get('fatherId') or None,
            data.get('motherId') or None,
            data['generation'],
            data['birthYear'],
            data['bloodGroup'],
            data['eyeColor'],
            data.get('birthmark'),
            data.get('disease'),
            data['passion'],
            data['trait'],
            data['nature'],
            data.get('about')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Family member registered successfully',
            'personId': person_id,
            'familyId': family_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

class FamilySearchEngine:
    def __init__(self):
        self.refresh_data()
        self.prepare_ml_features()
    
    def refresh_data(self):
        """Load data from PostgreSQL database"""
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('SELECT * FROM family_members')
        self.family_members = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Create lookup maps
        self.person_map = {member['person_id']: member for member in self.family_members}
        self.family_map = defaultdict(list)
        self.father_children_map = defaultdict(list)
        self.mother_children_map = defaultdict(list)
        
        for member in self.family_members:
            self.family_map[member['family_id']].append(member)
            if member.get('father_id'):
                self.father_children_map[member['father_id']].append(member)
            if member.get('mother_id'):
                self.mother_children_map[member['mother_id']].append(member)
    
    def prepare_ml_features(self):
        """Prepare text features for ML-based similarity search"""
        self.text_features = []
        for member in self.family_members:
            text = f"{member.get('first_name', '')} {member.get('last_name', '')} {member.get('passion', '')} {member.get('trait', '')} {member.get('nature', '')} {member.get('about', '')}"
            self.text_features.append(text.lower())
        
        if self.text_features:
            self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            try:
                self.tfidf_matrix = self.vectorizer.fit_transform(self.text_features)
            except ValueError:
                # Handle empty vocabulary (all stop words)
                self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
                self.tfidf_matrix = self.vectorizer.fit_transform(self.text_features or ['empty'])
        else:
            self.vectorizer = None
            self.tfidf_matrix = None
    
    def exact_match_search(self, query):
        """Traditional exact/partial match search"""
        results = []
        family_id = query.get('familyId')
        
        members_to_search = self.family_map[family_id] if family_id else self.family_members
        
        for member in members_to_search:
            match = True
            
            for field, value in query.items():
                if not value:
                    continue
                
                # Map frontend field names to database column names
                field_map = {
                    'firstName': 'first_name',
                    'lastName': 'last_name',
                    'personId': 'person_id',
                    'familyId': 'family_id',
                    'fatherId': 'father_id',
                    'motherId': 'mother_id',
                    'bloodGroup': 'blood_group',
                    'eyeColor': 'eye_color',
                    'birthYear': 'birth_year'
                }
                
                db_field = field_map.get(field, field)
                member_value = member.get(db_field)
                
                if member_value is None:
                    match = False
                    break
                
                if field in ['generation', 'birthYear']:
                    if int(member_value) != int(value):
                        match = False
                        break
                elif field in ['firstName', 'lastName', 'personId', 'familyId', 'bloodGroup', 'eyeColor']:
                    if str(member_value).lower() != str(value).lower():
                        match = False
                        break
                else:
                    if str(value).lower() not in str(member_value).lower():
                        match = False
                        break
            if match:
                results.append(member)
        
        return results
    
    def ml_similarity_search(self, query, threshold=0.1):
        """ML-based similarity search using TF-IDF and cosine similarity"""
        if not self.vectorizer or not self.tfidf_matrix:
            return []
            
        query_text = ""
        field_map = {
            'firstName': 'first_name', 
            'lastName': 'last_name'
        }
        
        for field, value in query.items():
            db_field = field_map.get(field, field)
            if value and db_field in ['first_name', 'last_name', 'passion', 'trait', 'nature']:
                query_text += f" {value}"
        
        if not query_text.strip():
            return []
        
        query_vector = self.vectorizer.transform([query_text.lower()])
        
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        results = []
        family_id = query.get('familyId')
        for i, similarity in enumerate(similarities):
            if similarity > threshold:
                member = self.family_members[i]
                if family_id and member['family_id'] != family_id:
                    continue
                member = dict(member)
                member['similarity_score'] = float(similarity)
                results.append(member)
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results
    def search(self, query):
        """Main search function combining exact match and ML similarity"""
        if not query:
            family_id = query.get('familyId')
            if family_id:
                return self.family_map[family_id]
            return self.family_members
        
        exact_results = self.exact_match_search(query)
        if exact_results:
            return exact_results
        
        ml_results = self.ml_similarity_search(query)
        if ml_results:
            return ml_results     
        return []

# Initialize search engine after database is initialized
search_engine = None

@app.route('/search', methods=['POST'])
def search_families():
    try:
        query = request.get_json() or {}
        clean_query = {k: v for k, v in query.items() if v and str(v).strip()}
        
        print(f"Search Query: {clean_query}")
        
        # Refresh data from database before search
        search_engine.refresh_data()
        
        # Perform search
        results = search_engine.search(clean_query)
        
        # Map database column names to frontend field names
        mapped_results = []
        for result in results:
            mapped_result = {
                'personId': result.get('person_id'),
                'firstName': result.get('first_name'),
                'lastName': result.get('last_name'),
                'familyId': result.get('family_id'),
                'fatherId': result.get('father_id'),
                'motherId': result.get('mother_id'),
                'generation': result.get('generation'),
                'birthYear': result.get('birth_year'),
                'bloodGroup': result.get('blood_group'),
                'eyeColor': result.get('eye_color'),
                'birthmark': result.get('birthmark'),
                'disease': result.get('disease'),
                'passion': result.get('passion'),
                'trait': result.get('trait'),
                'nature': result.get('nature'),
                'about': result.get('about'),
                'similarity_score': result.get('similarity_score')
            }
            mapped_results.append(mapped_result)
        
        print(f"Found {len(mapped_results)} results")
        
        return jsonify(mapped_results)
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Kul Setu ML Search Backend is running'})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    search_engine.refresh_data()
    stats = {
        'total_members': len(search_engine.family_members),
        'total_families': len(search_engine.family_map),
        'families': {fid: len(members) for fid, members in search_engine.family_map.items()}
    }
    return jsonify(stats)

if __name__ == '__main__':
    print("Starting Kul Setu ML Search Backend...")
    print("Initializing PostgreSQL database...")
    
    init_db()
    search_engine = FamilySearchEngine()
    
    print(f"Database connected: {len(search_engine.family_members)} members loaded")
    print(f"Families: {len(search_engine.family_map)}")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
