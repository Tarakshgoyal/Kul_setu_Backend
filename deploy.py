#!/usr/bin/env python3
"""
Deployment script to initialize external database and load CSV data
"""
import os
import sys
import csv
from datetime import datetime
import psycopg2

# Database connection parameters
DATABASE_URL = "postgresql://kul_setu_db_user:5xvepfwEtYa0Bzx89vyTiTnUqkJWG437@dpg-d3kjv2ffte5s738ehdh0-a.oregon-postgres.render.com/kul_setu_db"

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL)

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

def create_table():
    """Create the family_members table if it doesn't exist"""
    conn = get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'family_members'
        );
    """)
    
    table_exists = cur.fetchone()[0]
    
    if table_exists:
        print("Table 'family_members' already exists. Dropping and recreating...")
        cur.execute('DROP TABLE family_members')
    
    print("Creating family_members table...")
    cur.execute('''
        CREATE TABLE family_members (
            person_id VARCHAR(50) PRIMARY KEY,
            family_line_id VARCHAR(50) NOT NULL,
            generation INTEGER NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            gender VARCHAR(20) NOT NULL,
            ethnicity VARCHAR(100),
            mother_id VARCHAR(50),
            father_id VARCHAR(50),
            spouse_id VARCHAR(50),
            shared_ancestry_key VARCHAR(100),
            dob DATE,
            dod DATE,
            longevity_avg_lifespan DECIMAL(5,2),
            generation_avg_lifespan DECIMAL(5,2),
            cause_of_death VARCHAR(200),
            eye_color VARCHAR(30),
            hair_color VARCHAR(30),
            skin_tone VARCHAR(30),
            blood_group VARCHAR(10),
            birthmark VARCHAR(100),
            freckles VARCHAR(20),
            baldness VARCHAR(20),
            beard_style_trend VARCHAR(50),
            condition_diabetes VARCHAR(20),
            condition_heart_issue VARCHAR(20),
            condition_asthma VARCHAR(20),
            condition_color_blindness VARCHAR(20),
            left_handed VARCHAR(20),
            is_twin VARCHAR(20),
            nature_of_person VARCHAR(100),
            recipes_cuisine TEXT,
            family_traditions TEXT,
            native_location VARCHAR(200),
            migration_path VARCHAR(500),
            socioeconomic_status VARCHAR(50),
            education_level VARCHAR(50)
        )
    ''')
    
    cur.close()
    conn.close()
    print("✅ Table created successfully!")

def load_csv_data():
    """Load data from tree.csv into the database"""
    csv_file_path = 'tree.csv'
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file {csv_file_path} not found!")
        return False
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("Loading CSV data...")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        count = 0
        
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
            count += 1
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Successfully loaded {count} records from CSV into database")
    return True

def verify_data():
    """Verify that data was loaded correctly"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Count total records
    cur.execute("SELECT COUNT(*) FROM family_members;")
    total_count = cur.fetchone()[0]
    print(f"Total records in database: {total_count}")
    
    # Count unique family lines
    cur.execute("SELECT COUNT(DISTINCT family_line_id) FROM family_members;")
    family_lines = cur.fetchone()[0]
    print(f"Unique family lines: {family_lines}")
    
    # Show sample data
    cur.execute("SELECT person_id, first_name, family_line_id, generation FROM family_members LIMIT 5;")
    sample_data = cur.fetchall()
    print("\nSample data:")
    for row in sample_data:
        print(f"  {row[0]} - {row[1]} (Family: {row[2]}, Gen: {row[3]})")
    
    cur.close()
    conn.close()

def main():
    """Main deployment function"""
    print("🚀 Starting database deployment...")
    
    try:
        # Test connection
        print("\n1. Testing database connection...")
        conn = get_db_connection()
        conn.close()
        print("✅ Database connection successful!")
        
        # Create table
        print("\n2. Creating table...")
        create_table()
        
        # Load CSV data
        print("\n3. Loading CSV data...")
        if load_csv_data():
            # Verify data
            print("\n4. Verifying data...")
            verify_data()
            
            print("\n🎉 Deployment completed successfully!")
        else:
            print("\n❌ Deployment failed during CSV loading")
            return False
            
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()