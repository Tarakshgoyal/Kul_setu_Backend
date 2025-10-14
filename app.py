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
import hashlib

app = Flask(__name__)
CORS(app)

# Database configuration - using external Render PostgreSQL
DATABASE_URL = "postgresql://kul_setu_db_user:5xvepfwEtYa0Bzx89vyTiTnUqkJWG437@dpg-d3kjv2ffte5s738ehdh0-a.oregon-postgres.render.com/kul_setu_db"

def get_db_connection():
    """Get database connection with timeout"""
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=30)
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def init_db():
    # Connect to external database
    conn = get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if table exists, if not create it
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'family_members'
        );
    """)
    
    table_exists = cur.fetchone()[0]
    
    if not table_exists:
        print("Creating family_members table...")
        # Create table with new schema
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
            other_disease VARCHAR(200),
            passion VARCHAR(100),
            disability VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table for authentication
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(50) PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            family_id VARCHAR(50),
            person_id VARCHAR(50),
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
        return False
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Clear existing data
        print("Clearing existing data...")
        cur.execute('DELETE FROM family_members')
        print("Existing data cleared.")
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            count = 0
            
            print("Reading CSV file...")
            for row in csv_reader:
                try:
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
                            migration_path, socioeconomic_status, education_level, other_disease, passion, disability
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                        row['Education_Level'],
                        row.get('Other_Disease', None),  # New field, optional in CSV
                        row.get('Passion', None),  # New field, optional in CSV
                        row.get('Disability', None)  # New field, optional in CSV
                    ))
                    count += 1
                    if count % 100 == 0:
                        print(f"Processed {count} records...")
                        
                except Exception as e:
                    print(f"Error processing row {count + 1}: {e}")
                    print(f"Row data: {row}")
                    continue
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully loaded {count} records from CSV into database")
        
        # Sync users table with CSV email/password data
        sync_users_from_csv()
        
        return True
        
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return False

def sync_users_from_csv():
    """Sync users table with email/password data from CSV"""
    try:
        print("Syncing users table with CSV email/password data...")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Read CSV to get email and password data
        with open('tree.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            added_count = 0
            for row in csv_reader:
                person_id = row.get('Person_ID')
                first_name = row.get('First_Name', '').replace('_', ' ').title()
                family_id = row.get('Family_Line_ID')
                email = row.get('Email')
                password_hash = row.get('Password')  # Already hashed
                
                if not all([person_id, first_name, family_id, email, password_hash]):
                    continue
                
                # Check if user already exists
                cur.execute('SELECT user_id FROM users WHERE email = %s', (email,))
                if cur.fetchone():
                    continue  # Skip if user already exists
                
                # Insert new user
                user_id = f"U{person_id[1:]}"  # Convert P0001 to U0001
                try:
                    cur.execute('''
                        INSERT INTO users (user_id, email, password_hash, first_name, last_name, family_id, person_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (user_id, email, password_hash, first_name, '', family_id, person_id))
                    added_count += 1
                except Exception as e:
                    # Skip duplicates
                    continue
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Users synced: {added_count} new users added to authentication system")
        
    except Exception as e:
        print(f"Error syncing users: {e}")

def generate_id():
    return str(uuid.uuid4())[:8].upper()

def validate_alive_member(data):
    """Validate data for alive family member"""
    required_fields = ['firstName', 'gender', 'generation', 'dob']
    for field in required_fields:
        if not data.get(field):
            return False, f"Required field missing: {field}"
    
    # Validate that DOD is not provided for alive members
    if data.get('dod'):
        return False, "Date of death should not be provided for alive members"
    
    # Validate that cause of death is not provided for alive members
    if data.get('causeOfDeath'):
        return False, "Cause of death should not be provided for alive members"
    
    return True, ""

def validate_dead_member(data):
    """Validate data for deceased family member"""
    required_fields = ['firstName', 'gender', 'generation', 'dob', 'dod', 'causeOfDeath']
    for field in required_fields:
        if not data.get(field):
            return False, f"Required field missing: {field}"
    
    # Validate that DOD is after DOB
    try:
        dob = parse_date(data.get('dob'))
        dod = parse_date(data.get('dod'))
        if dob and dod and dod <= dob:
            return False, "Date of death must be after date of birth"
    except:
        return False, "Invalid date format"
    
    return True, ""

@app.route('/register/alive', methods=['POST'])
def register_alive_member():
    """Register a living family member"""
    try:
        data = request.get_json()
        
        # Validate alive member data
        is_valid, error_msg = validate_alive_member(data)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Generate IDs if not provided
        person_id = data.get('personId') or generate_id()
        family_line_id = data.get('familyLineId') or generate_id()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # For alive members, DOD and cause_of_death should be NULL
        cur.execute('''
            INSERT INTO family_members (
                person_id, family_line_id, generation, first_name, gender, ethnicity,
                mother_id, father_id, spouse_id, shared_ancestry_key, dob, dod,
                longevity_avg_lifespan, generation_avg_lifespan, cause_of_death,
                eye_color, hair_color, skin_tone, blood_group, birthmark, freckles,
                baldness, beard_style_trend, condition_diabetes, condition_heart_issue,
                condition_asthma, condition_color_blindness, left_handed, is_twin,
                nature_of_person, recipes_cuisine, family_traditions, native_location,
                migration_path, socioeconomic_status, education_level, other_disease, passion, disability
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            None,  # DOD is NULL for alive members
            parse_decimal(data.get('longevityAvgLifespan')),
            parse_decimal(data.get('generationAvgLifespan')),
            None,  # Cause of death is NULL for alive members
            data.get('eyeColor'),
            data.get('hairColor'),
            data.get('skinTone'),
            data.get('bloodGroup'),
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
            data.get('natureOfPerson'),
            data.get('recipesCuisine'),
            data.get('familyTraditions'),
            data.get('nativeLocation'),
            data.get('migrationPath'),
            data.get('socioeconomicStatus'),
            data.get('educationLevel'),
            data.get('otherDisease'),
            None,  # Passion is NULL for alive members
            data.get('disability')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Alive family member registered successfully',
            'personId': person_id,
            'familyLineId': family_line_id,
            'status': 'alive'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/register/dead', methods=['POST'])
def register_dead_member():
    """Register a deceased family member"""
    try:
        data = request.get_json()
        
        # Validate dead member data
        is_valid, error_msg = validate_dead_member(data)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
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
                migration_path, socioeconomic_status, education_level, other_disease, passion, disability
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            data.get('eyeColor'),
            data.get('hairColor'),
            data.get('skinTone'),
            data.get('bloodGroup'),
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
            data.get('natureOfPerson'),
            data.get('recipesCuisine'),
            data.get('familyTraditions'),
            data.get('nativeLocation'),
            data.get('migrationPath'),
            data.get('socioeconomicStatus'),
            data.get('educationLevel'),
            data.get('otherDisease'),
            data.get('passion'),
            data.get('disability')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Deceased family member registered successfully',
            'personId': person_id,
            'familyLineId': family_line_id,
            'status': 'deceased'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register_member():
    """Legacy registration endpoint - redirects to appropriate specific endpoint"""
    try:
        data = request.get_json()
        
        # Check if member is alive or dead based on provided data
        if data.get('dod') or data.get('causeOfDeath'):
            # Has death information, treat as deceased
            return register_dead_member()
        else:
            # No death information, treat as alive
            return register_alive_member()
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/register/schema', methods=['GET'])
def get_registration_schema():
    """Get registration form schema for both alive and dead members"""
    return jsonify({
        'alive': {
            'required_fields': ['firstName', 'gender', 'generation', 'dob'],
            'optional_fields': [
                'ethnicity', 'motherId', 'fatherId', 'spouseId', 'sharedAncestryKey',
                'longevityAvgLifespan', 'generationAvgLifespan', 'eyeColor', 'hairColor',
                'skinTone', 'bloodGroup', 'birthmark', 'freckles', 'baldness',
                'beardStyleTrend', 'conditionDiabetes', 'conditionHeartIssue',
                'conditionAsthma', 'conditionColorBlindness', 'leftHanded', 'isTwin',
                'natureOfPerson', 'recipesCuisine', 'familyTraditions', 'nativeLocation',
                'migrationPath', 'socioeconomicStatus', 'educationLevel'
            ],
            'excluded_fields': ['dod', 'causeOfDeath'],
            'validation_rules': {
                'dob': 'Must be a valid date in DD-MM-YYYY format',
                'dod': 'Should NOT be provided for alive members',
                'causeOfDeath': 'Should NOT be provided for alive members'
            }
        },
        'dead': {
            'required_fields': ['firstName', 'gender', 'generation', 'dob', 'dod', 'causeOfDeath'],
            'optional_fields': [
                'ethnicity', 'motherId', 'fatherId', 'spouseId', 'sharedAncestryKey',
                'longevityAvgLifespan', 'generationAvgLifespan', 'eyeColor', 'hairColor',
                'skinTone', 'bloodGroup', 'birthmark', 'freckles', 'baldness',
                'beardStyleTrend', 'conditionDiabetes', 'conditionHeartIssue',
                'conditionAsthma', 'conditionColorBlindness', 'leftHanded', 'isTwin',
                'natureOfPerson', 'recipesCuisine', 'familyTraditions', 'nativeLocation',
                'migrationPath', 'socioeconomicStatus', 'educationLevel'
            ],
            'validation_rules': {
                'dob': 'Must be a valid date in DD-MM-YYYY format',
                'dod': 'Must be a valid date in DD-MM-YYYY format and after DOB',
                'causeOfDeath': 'Must specify cause of death for deceased members'
            }
        },
        'field_options': {
            'gender': ['M', 'F', 'Other'],
            'ethnicity': ['East Asian', 'South Asian', 'Western European', 'African', 'Mixed', 'Other'],
            'bloodGroup': ['A', 'B', 'AB', 'O', 'A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-'],
            'eyeColor': ['Brown', 'Blue', 'Green', 'Hazel', 'Gray', 'Amber'],
            'hairColor': ['Black', 'Brown', 'Blonde', 'Red', 'Gray', 'White'],
            'skinTone': ['Light', 'Medium', 'Dark'],
            'birthmark': ['None', 'Forehead', 'Cheek', 'Neck', 'Shoulder', 'Back', 'Chest', 'Arm', 'Wrist', 'Hand', 'Thigh', 'Knee', 'Ankle', 'Foot', 'Hip', 'Waist', 'Upper_Back', 'Lower_Back', 'Shin', 'Calf', 'Elbow', 'Forearm', 'Palm', 'Finger', 'Toe', 'Abdomen'],
            'yesNoFields': ['freckles', 'baldness', 'conditionDiabetes', 'conditionHeartIssue', 'conditionAsthma', 'conditionColorBlindness', 'leftHanded', 'isTwin'],
            'beardStyleTrend': ['Full Beard', 'Moustache', 'Stubble', 'Clean Shaven', 'Goatee'],
            'natureOfPerson': ['Aggressive', 'Calm', 'Artistic', 'Extrovert', 'Introvert', 'Spiritual'],
            'socioeconomicStatus': ['Low', 'Medium', 'High'],
            'educationLevel': ['High School', 'Bachelor\'s', 'Master\'s', 'PhD'],
            'causeOfDeath': ['Old Age', 'Accident', 'Infection', 'Heart Disease', 'Cancer', 'Stroke', 'Natural Causes', 'Unknown']
        }
    })

@app.route('/register/validate', methods=['POST'])
def validate_registration_data():
    """Validate registration data before submission"""
    try:
        data = request.get_json()
        member_type = data.get('type', 'alive')  # Default to alive
        member_data = data.get('data', {})
        
        if member_type == 'alive':
            is_valid, error_msg = validate_alive_member(member_data)
        elif member_type == 'dead':
            is_valid, error_msg = validate_dead_member(member_data)
        else:
            return jsonify({'valid': False, 'error': 'Invalid member type. Must be "alive" or "dead"'}), 400
        
        return jsonify({
            'valid': is_valid,
            'error': error_msg if not is_valid else None,
            'type': member_type
        })
        
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

class FamilySearchEngine:
    def __init__(self):
        self.family_members = []
        self.person_map = {}
        self.family_map = defaultdict(list)
        self.father_children_map = defaultdict(list)
        self.mother_children_map = defaultdict(list)
        self.vectorizer = None
        self.tfidf_matrix = None
        
        try:
            self.refresh_data()
            self.prepare_ml_features()
        except Exception as e:
            print(f"Warning: Failed to initialize search engine data: {e}")
            print("Search engine initialized with empty data. Use /init-db to populate.")
    
    def refresh_data(self):
        """Load data from PostgreSQL database"""
        try:
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
        except Exception as e:
            print(f"Error refreshing data: {e}")
            self.family_members = []
            self.person_map = {}
            self.family_map = defaultdict(list)
            self.father_children_map = defaultdict(list)
            self.mother_children_map = defaultdict(list)
    
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
            print("No text features available - ML search will be disabled")
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

# Initialize search engine 
search_engine = None

def get_search_engine():
    """Get or initialize the search engine"""
    global search_engine
    if search_engine is None:
        print("Initializing search engine...")
        search_engine = FamilySearchEngine()
    return search_engine

@app.route('/search', methods=['POST'])
def search_families():
    try:
        query = request.get_json() or {}
        clean_query = {k: v for k, v in query.items() if v and str(v).strip()}
        
        print(f"Search Query: {clean_query}")
        
        # Get or initialize search engine
        engine = get_search_engine()
        
        # Refresh data from database before search
        engine.refresh_data()
        
        # Perform search
        results = engine.search(clean_query)
        
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
        import traceback
        traceback.print_exc()
        # Return empty array instead of error object to prevent frontend crashes
        return jsonify([]), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Kul Setu Backend API', 'status': 'running', 'version': '1.0'})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Kul Setu ML Search Backend is running'})

@app.route('/init-db', methods=['POST'])
def initialize_database():
    """Initialize database and load sample data if CSV is not available"""
    try:
        # First try to initialize the database
        init_db()
        
        # Try to load CSV data
        csv_loaded = load_csv_data()
        
        # If CSV loading failed, create some sample data
        if not csv_loaded:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Check if table is empty
            cur.execute('SELECT COUNT(*) FROM family_members')
            count = cur.fetchone()[0]
            
            if count == 0:
                # Insert sample data
                sample_data = [
                    ('SAMPLE001', 'F01', 1, 'John Doe', 'M', 'European', None, None, 'SAMPLE002', 'ANCS001', 
                     '1990-01-01', None, None, None, None, 'Brown', 'Black', 'Light', 'O+', 'No', 'No', 'No', 
                     None, 'No', 'No', 'No', 'No', 'No', 'No', 'Friendly', 'Italian', 'Christmas Traditions', 
                     'New York', None, 'Middle', 'Bachelor'),
                    ('SAMPLE002', 'F01', 1, 'Jane Smith', 'F', 'European', None, None, 'SAMPLE001', 'ANCS001',
                     '1992-03-15', None, None, None, None, 'Blue', 'Blonde', 'Light', 'A+', 'No', 'No', 'No',
                     None, 'No', 'No', 'No', 'No', 'No', 'No', 'Kind', 'French', 'New Year Traditions',
                     'California', None, 'Middle', 'Master')
                ]
                
                for data in sample_data:
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
                    ''', data)
                
                conn.commit()
                message = "Database initialized with sample data"
            else:
                message = f"Database already contains {count} records"
            
            cur.close()
            conn.close()
        else:
            message = "Database initialized and CSV data loaded successfully"
        
        return jsonify({'success': True, 'message': message})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        engine = get_search_engine()
        engine.refresh_data()
        stats = {
            'total_members': len(engine.family_members),
            'total_families': len(engine.family_map),
            'families': {fid: len(members) for fid, members in engine.family_map.items()}
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e), 'total_members': 0, 'total_families': 0}), 500

@app.route('/reload-csv', methods=['POST'])
def reload_csv():
    """Reload CSV data into database"""
    try:
        load_csv_data()
        engine = get_search_engine()
        engine.refresh_data()
        engine.prepare_ml_features()
        return jsonify({
            'success': True, 
            'message': f'Successfully reloaded {len(engine.family_members)} members from CSV'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    """Verify password against hash"""
    return hash_password(password) == stored_hash

@app.route('/auth/signup', methods=['POST'])
def auth_signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        family_id = data.get('familyId')
        person_id = data.get('personId')
        
        if not all([email, password, first_name, last_name]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if email already exists
        cur.execute('SELECT email FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Generate user ID
        user_id = str(uuid.uuid4())[:8].upper()
        
        # Handle family_id and person_id logic
        if family_id:
            # Verify family exists
            cur.execute('SELECT family_line_id FROM family_members WHERE family_line_id = %s LIMIT 1', (family_id,))
            if not cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({'success': False, 'error': 'Family ID not found'}), 400
            
            # If person_id provided, verify it exists in the family
            if person_id:
                cur.execute('SELECT person_id FROM family_members WHERE person_id = %s AND family_line_id = %s', (person_id, family_id))
                if not cur.fetchone():
                    cur.close()
                    conn.close()
                    return jsonify({'success': False, 'error': 'Person ID not found in the specified family'}), 400
            else:
                # Generate new person ID for this family
                cur.execute('SELECT MAX(CAST(SUBSTRING(person_id FROM 2) AS INTEGER)) FROM family_members WHERE family_line_id = %s', (family_id,))
                max_person_num = cur.fetchone()[0] or 0
                person_id = f"P{max_person_num + 1:04d}"
        else:
            # Generate new family ID and person ID
            cur.execute('SELECT MAX(CAST(SUBSTRING(family_line_id FROM 2) AS INTEGER)) FROM family_members')
            max_family_num = cur.fetchone()[0] or 0
            family_id = f"F{max_family_num + 1:02d}"
            person_id = f"P{1:04d}" if not person_id else person_id
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert user
        cur.execute('''
            INSERT INTO users (user_id, email, password_hash, first_name, last_name, family_id, person_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, email, password_hash, first_name, last_name, family_id, person_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'userId': user_id,
            'familyId': family_id,
            'personId': person_id,
            'message': 'User registered successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def auth_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'success': False, 'error': 'Missing email or password'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get user by email
        cur.execute('''
            SELECT user_id, email, password_hash, first_name, last_name, family_id, person_id
            FROM users WHERE email = %s
        ''', (email,))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user or not verify_password(password, user['password_hash']):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['user_id'],
                'email': user['email'],
                'firstName': user['first_name'],
                'lastName': user['last_name'],
                'familyId': user['family_id'],
                'personId': user['person_id']
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Kul Setu ML Search Backend...")
    
    try:
        print("Testing database connection...")
        conn = get_db_connection()
        conn.close()
        print("✅ Database connection successful!")
        
        print("Initializing PostgreSQL database...")
        init_db()
        
        print("Skipping CSV loading on startup (will load on demand)")
        print("You can initialize database with sample data by calling: /init-db")
        
        print("Initializing search engine...")
        search_engine = FamilySearchEngine()
        
        print(f"Database ready: {len(search_engine.family_members)} members currently loaded")
        print(f"Families: {len(search_engine.family_map)}")
        
        if len(search_engine.family_members) == 0:
            print("⚠️  No data loaded. Call POST /init-db to initialize with sample data.")
        
        print("🚀 Starting Flask server on http://127.0.0.1:5000")
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        import traceback
        traceback.print_exc()
