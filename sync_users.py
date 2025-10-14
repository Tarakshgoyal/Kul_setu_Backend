import csv
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib

def get_db_connection():
    """Get database connection using the same connection string as app.py"""
    try:
        conn = psycopg2.connect("postgresql://kul_setu_user:password@dpg-cuhd6c68ii6s73a1llr0-a.oregon-postgres.render.com/kul_setu")
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def sync_csv_to_users_table():
    """Sync CSV email/password data to users table"""
    
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database!")
        return
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Read CSV data
        print("Reading CSV data...")
        with open('tree.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)
        
        print(f"Found {len(csv_data)} records in CSV")
        
        # Get current users in database
        cur.execute('SELECT email, person_id FROM users')
        existing_users = {row['email']: row['person_id'] for row in cur.fetchall()}
        
        print(f"Found {len(existing_users)} existing users in database")
        
        # Process each CSV record
        added_count = 0
        updated_count = 0
        
        for row in csv_data:
            person_id = row.get('Person_ID')
            first_name = row.get('First_Name', '').replace('_', ' ').title()
            family_id = row.get('Family_Line_ID')
            email = row.get('Email')
            password_hash = row.get('Password')  # Already hashed
            
            if not all([person_id, first_name, family_id, email, password_hash]):
                print(f"Skipping incomplete record: {person_id}")
                continue
            
            # Check if user exists
            if email in existing_users:
                # Update existing user
                cur.execute('''
                    UPDATE users 
                    SET first_name = %s, last_name = %s, family_id = %s, person_id = %s, password_hash = %s
                    WHERE email = %s
                ''', (first_name, '', family_id, person_id, password_hash, email))
                updated_count += 1
                if updated_count <= 5:  # Show first few updates
                    print(f"Updated: {email} → {person_id}")
            else:
                # Insert new user
                user_id = f"U{person_id[1:]}"  # Convert P0001 to U0001
                cur.execute('''
                    INSERT INTO users (user_id, email, password_hash, first_name, last_name, family_id, person_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (user_id, email, password_hash, first_name, '', family_id, person_id))
                added_count += 1
                if added_count <= 5:  # Show first few additions
                    print(f"Added: {email} → {person_id}")
        
        conn.commit()
        print(f"\n✅ Sync completed!")
        print(f"📝 Added {added_count} new users")
        print(f"🔄 Updated {updated_count} existing users")
        print(f"👥 Total users in database: {added_count + len(existing_users)}")
        
        # Test login with a sample user
        print(f"\n🧪 Testing login...")
        sample_email = "person1.p0001@kulsetufamily.com"
        sample_password = "p0001123"
        
        cur.execute('SELECT * FROM users WHERE email = %s', (sample_email,))
        user = cur.fetchone()
        
        if user:
            stored_hash = user['password_hash']
            test_hash = hash_password(sample_password)
            
            if stored_hash == test_hash:
                print(f"✅ Login test successful for {sample_email}")
                print(f"   User ID: {user['user_id']}")
                print(f"   Person ID: {user['person_id']}")
                print(f"   Family ID: {user['family_id']}")
            else:
                print(f"❌ Password hash mismatch for {sample_email}")
        else:
            print(f"❌ Sample user {sample_email} not found")
        
    except Exception as e:
        print(f"Error syncing data: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    sync_csv_to_users_table()