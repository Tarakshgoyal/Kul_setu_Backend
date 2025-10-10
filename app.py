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
import csv
from datetime import datetime

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
    
    # Drop existing table to recreate with new schema
    cur.execute('DROP TABLE IF EXISTS family_members')
    
    cur.execute('''
        CREATE TABLE family_members (
            person_id VARCHAR(50) PRIMARY KEY,
            family_line_id VARCHAR(50) NOT NULL,
            generation INTEGER NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            ethnicity VARCHAR(50),
            mother_id VARCHAR(50),
            father_id VARCHAR(50),
            spouse_id VARCHAR(50),
            shared_ancestry_key VARCHAR(50),
            dob DATE,
            dod DATE,
            longevity_avg_lifespan DECIMAL(10,8),
            generation_avg_lifespan DECIMAL(10,8),
            cause_of_death VARCHAR(50),
            eye_color VARCHAR(20),
            hair_color VARCHAR(20),
            skin_tone VARCHAR(20),
            blood_group VARCHAR(10),
            birthmark VARCHAR(10),
            freckles VARCHAR(10),
            baldness VARCHAR(10),
            beard_style_trend VARCHAR(50),
            condition_diabetes VARCHAR(10),
            condition_heart_issue VARCHAR(10),
            condition_asthma VARCHAR(10),
            condition_color_blindness VARCHAR(10),
            left_handed VARCHAR(10),
            is_twin VARCHAR(10),
            nature_of_person VARCHAR(50),
            recipes_cuisine VARCHAR(50),
            family_traditions VARCHAR(50),
            native_location VARCHAR(100),
            migration_path VARCHAR(200),
            socioeconomic_status VARCHAR(20),
            education_level VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def parse_date(date_str):
    """Parse date string in DD-MM-YYYY format to PostgreSQL date"""
    if not date_str or date_str == 'N/A':
        return None
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None

def parse_decimal(value_str):
    """Parse decimal string to float"""
    if not value_str or value_str == 'N/A':
        return None
    try:
        return float(value_str)
    except ValueError:
        return None

def load_csv_data():
    """Load data from tree.csv into the database"""
    csv_file_path = 'tree.csv'
    if not os.path.exists(csv_file_path):
        print(f"CSV file {csv_file_path} not found!")
        return
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Clear existing data
    cur.execute('DELETE FROM family_members')
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Convert 'N/A' to None for foreign keys
            mother_id = row['Mother_ID'] if row['Mother_ID'] != 'N/A' else None
            father_id = row['Father_ID'] if row['Father_ID'] != 'N/A' else None
            spouse_id = row['Spouse_ID'] if row['Spouse_ID'] != 'N/A' else None
            migration_path = row['Migration_Path'] if row['Migration_Path'] != '' else None
            
            cur.execute('''
                INSERT INTO family_members (
                    person_id, family_line_id, generation, first_name, gender, ethnicity,
                    mother_id, father_id, spouse_id, shared_ancestry_key, dob, dod,
                    longevity_avg_lifespan, generation_avg_lifespan, cause_of_death,
                    eye_color, hair_color, skin_tone, blood_group, birthmark, freckles,
                    baldness, beard_style_trend, condition_diabetes, condition_heart_issue,
                    condition_asthma, condition_color_blindness, left_handed, is_twin,
                    nature_of_person, recipes_cuisine, family_traditions, native_location,
                    migration_path, socioeconomic_status, education_level
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                row['Person_ID'],
                row['Family_Line_ID'],
                int(row['Generation']),
                row['First_Name'],
                row['Gender'],
                row['Ethnicity'],
                mother_id,
                father_id,
                spouse_id,
                row['Shared_Ancestry_Key'],
                parse_date(row['DOB']),
                parse_date(row['DOD']),
                parse_decimal(row['Longevity_Avg_Lifespan']),
                parse_decimal(row['Generation_Avg_Lifespan']),
                row['Cause_of_Death'] if row['Cause_of_Death'] != 'N/A' else None,
                row['Eye_Color'],
                row['Hair_Color'],
                row['Skin_Tone'],
                row['Blood_Group'],
                row['Birthmark'],
                row['Freckles'],
                row['Baldness'],
                row['Beard_Style_Trend'] if row['Beard_Style_Trend'] != 'N/A' else None,
                row['Condition_Diabetes'],
                row['Condition_Heart_Issue'],
                row['Condition_Asthma'],
                row['Condition_Color_Blindness'],
                row['Left_Handed'],
                row['Is_Twin'],
                row['Nature_of_Person'],
                row['Recipes_Cuisine'],
                row['Family_Traditions'],
                row['Native_Location'],
                migration_path,
                row['Socioeconomic_Status'],
                row['Education_Level']
            ))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Successfully loaded CSV data into database")

def generate_id():
    return str(uuid.uuid4())[:8].upper()
@app.route('/register', methods=['POST'])
def register_member():
    try:
        data = request.get_json()
        
        # Generate IDs if not provided
        person_id = data.get('personId') or generate_id()
        family_line_id = data.get('familyLineId') or generate_id()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO family_members (
                person_id, family_line_id, generation, first_name, gender, ethnicity,
                mother_id, father_id, spouse_id, shared_ancestry_key, dob, dod,
                longevity_avg_lifespan, generation_avg_lifespan, cause_of_death,
                eye_color, hair_color, skin_tone, blood_group, birthmark, freckles,
                baldness, beard_style_trend, condition_diabetes, condition_heart_issue,
                condition_asthma, condition_color_blindness, left_handed, is_twin,
                nature_of_person, recipes_cuisine, family_traditions, native_location,
                migration_path, socioeconomic_status, education_level
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            person_id,
            family_line_id,
            data['generation'],
            data['firstName'],
            data['gender'],
            data.get('ethnicity'),
            data.get('motherId'),
            data.get('fatherId'),
            data.get('spouseId'),
            data.get('sharedAncestryKey'),
            parse_date(data.get('dob')),
            parse_date(data.get('dod')),
            parse_decimal(data.get('longevityAvgLifespan')),
            parse_decimal(data.get('generationAvgLifespan')),
            data.get('causeOfDeath'),
            data['eyeColor'],
            data.get('hairColor'),
            data.get('skinTone'),
            data['bloodGroup'],
            data.get('birthmark'),
            data.get('freckles'),
            data.get('baldness'),
            data.get('beardStyleTrend'),
            data.get('conditionDiabetes'),
            data.get('conditionHeartIssue'),
            data.get('conditionAsthma'),
            data.get('conditionColorBlindness'),
            data.get('leftHanded'),
            data.get('isTwin'),
            data['natureOfPerson'],
            data.get('recipesCuisine'),
            data.get('familyTraditions'),
            data.get('nativeLocation'),
            data.get('migrationPath'),
            data.get('socioeconomicStatus'),
            data.get('educationLevel')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Family member registered successfully',
            'personId': person_id,
            'familyLineId': family_line_id
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
            self.family_map[member['family_line_id']].append(member)
            if member.get('father_id'):
                self.father_children_map[member['father_id']].append(member)
            if member.get('mother_id'):
                self.mother_children_map[member['mother_id']].append(member)
    
    def prepare_ml_features(self):
        """Prepare text features for ML-based similarity search"""
        self.text_features = []
        for member in self.family_members:
            text = f"{member.get('first_name', '')} {member.get('ethnicity', '')} {member.get('nature_of_person', '')} {member.get('recipes_cuisine', '')} {member.get('family_traditions', '')} {member.get('native_location', '')} {member.get('education_level', '')}"
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
        family_line_id = query.get('familyLineId')
        
        members_to_search = self.family_map[family_line_id] if family_line_id else self.family_members
        
        for member in members_to_search:
            match = True
            
            for field, value in query.items():
                if not value:
                    continue
                
                # Map frontend field names to database column names
                field_map = {
                    'firstName': 'first_name',
                    'personId': 'person_id',
                    'familyLineId': 'family_line_id',
                    'fatherId': 'father_id',
                    'motherId': 'mother_id',
                    'spouseId': 'spouse_id',
                    'bloodGroup': 'blood_group',
                    'eyeColor': 'eye_color',
                    'hairColor': 'hair_color',
                    'skinTone': 'skin_tone',
                    'natureOfPerson': 'nature_of_person',
                    'recipesCuisine': 'recipes_cuisine',
                    'familyTraditions': 'family_traditions',
                    'nativeLocation': 'native_location',
                    'migrationPath': 'migration_path',
                    'socioeconomicStatus': 'socioeconomic_status',
                    'educationLevel': 'education_level'
                }
                
                db_field = field_map.get(field, field)
                member_value = member.get(db_field)
                
                if member_value is None:
                    match = False
                    break
                
                if field in ['generation']:
                    if int(member_value) != int(value):
                        match = False
                        break
                elif field in ['firstName', 'personId', 'familyLineId', 'bloodGroup', 'eyeColor', 'gender', 'ethnicity']:
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
            'firstName': 'first_name'
        }
        
        for field, value in query.items():
            db_field = field_map.get(field, field)
            if value and db_field in ['first_name', 'ethnicity', 'nature_of_person', 'recipes_cuisine', 'family_traditions', 'native_location', 'education_level']:
                query_text += f" {value}"
        
        if not query_text.strip():
            return []
        
        query_vector = self.vectorizer.transform([query_text.lower()])
        
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        results = []
        family_line_id = query.get('familyLineId')
        for i, similarity in enumerate(similarities):
            if similarity > threshold:
                member = self.family_members[i]
                if family_line_id and member['family_line_id'] != family_line_id:
                    continue
                member = dict(member)
                member['similarity_score'] = float(similarity)
                results.append(member)
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results
    def search(self, query):
        """Main search function combining exact match and ML similarity"""
        if not query:
            family_line_id = query.get('familyLineId')
            if family_line_id:
                return self.family_map[family_line_id]
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
                'familyLineId': result.get('family_line_id'),
                'generation': result.get('generation'),
                'firstName': result.get('first_name'),
                'gender': result.get('gender'),
                'ethnicity': result.get('ethnicity'),
                'motherId': result.get('mother_id'),
                'fatherId': result.get('father_id'),
                'spouseId': result.get('spouse_id'),
                'sharedAncestryKey': result.get('shared_ancestry_key'),
                'dob': str(result.get('dob')) if result.get('dob') else None,
                'dod': str(result.get('dod')) if result.get('dod') else None,
                'longevityAvgLifespan': result.get('longevity_avg_lifespan'),
                'generationAvgLifespan': result.get('generation_avg_lifespan'),
                'causeOfDeath': result.get('cause_of_death'),
                'eyeColor': result.get('eye_color'),
                'hairColor': result.get('hair_color'),
                'skinTone': result.get('skin_tone'),
                'bloodGroup': result.get('blood_group'),
                'birthmark': result.get('birthmark'),
                'freckles': result.get('freckles'),
                'baldness': result.get('baldness'),
                'beardStyleTrend': result.get('beard_style_trend'),
                'conditionDiabetes': result.get('condition_diabetes'),
                'conditionHeartIssue': result.get('condition_heart_issue'),
                'conditionAsthma': result.get('condition_asthma'),
                'conditionColorBlindness': result.get('condition_color_blindness'),
                'leftHanded': result.get('left_handed'),
                'isTwin': result.get('is_twin'),
                'natureOfPerson': result.get('nature_of_person'),
                'recipesCuisine': result.get('recipes_cuisine'),
                'familyTraditions': result.get('family_traditions'),
                'nativeLocation': result.get('native_location'),
                'migrationPath': result.get('migration_path'),
                'socioeconomicStatus': result.get('socioeconomic_status'),
                'educationLevel': result.get('education_level'),
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

@app.route('/reload-csv', methods=['POST'])
def reload_csv():
    """Reload CSV data into database"""
    try:
        load_csv_data()
        search_engine.refresh_data()
        search_engine.prepare_ml_features()
        return jsonify({
            'success': True, 
            'message': f'Successfully reloaded {len(search_engine.family_members)} members from CSV'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Kul Setu ML Search Backend...")
    print("Initializing PostgreSQL database...")
    
    init_db()
    print("Loading CSV data...")
    load_csv_data()
    
    search_engine = FamilySearchEngine()
    
    print(f"Database connected: {len(search_engine.family_members)} members loaded")
    print(f"Families: {len(search_engine.family_map)}")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
