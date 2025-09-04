from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'kulsetudb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        port=os.getenv('DB_PORT', '5432')
    )

# Initialize database
def init_db():
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

@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('SELECT * FROM family_members ORDER BY created_at DESC')
        members = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify(list(members))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)