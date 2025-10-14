import csv
import hashlib

def generate_email(first_name, person_id):
    """Generate email based on first name and person ID"""
    return f"{first_name.lower().replace('_', '')}.{person_id.lower()}@kulsetufamily.com"

def generate_password_hash(password):
    """Generate SHA-256 hash of password"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_email_password_columns():
    """Add Email and Password columns to the CSV"""
    
    # Read the current CSV
    with open('tree.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    if len(rows) == 0:
        print("CSV file is empty!")
        return
    
    # Check if Email and Password columns already exist
    header = rows[0]
    if 'Email' in header and 'Password' in header:
        print("Email and Password columns already exist!")
        return
    
    # Add Email and Password to header
    header.extend(['Email', 'Password'])
    rows[0] = header
    
    # Get indices for required columns
    try:
        first_name_idx = header.index('First_Name')
        person_id_idx = header.index('Person_ID')
    except ValueError as e:
        print(f"Required column not found: {e}")
        return
    
    # Add email and password for each person
    for i in range(1, len(rows)):
        if len(rows[i]) > 0:
            first_name = rows[i][first_name_idx]
            person_id = rows[i][person_id_idx]
            
            # Generate email
            email = generate_email(first_name, person_id)
            
            # Generate a simple password (person_id + "123")
            simple_password = f"{person_id.lower()}123"
            password_hash = generate_password_hash(simple_password)
            
            # Add to row
            rows[i].extend([email, password_hash])
            
            print(f"Added: {email} with password: {simple_password}")
    
    # Write back to CSV
    with open('tree.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print(f"\n✅ Successfully added Email and Password columns!")
    print(f"📧 {len(rows)-1} family members now have login credentials")
    print("\n🔑 Password format: [person_id]123")
    print("Example: P0001 → password: p0001123")
    print("         P0002 → password: p0002123")

if __name__ == "__main__":
    add_email_password_columns()