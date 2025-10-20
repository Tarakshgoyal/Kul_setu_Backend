import csv
import os

print('=== CSV Validation ===')

if os.path.exists('tree.csv'):
    print(f'CSV file size: {os.path.getsize("tree.csv")} bytes')
    
    with open('tree.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print(f'Headers: {len(headers)} columns')
        print(f'Has Email: {"Email" in headers}')
        print(f'Has Password: {"Password" in headers}')
        
        rows = list(reader)
        print(f'Rows: {len(rows)}')
        
        if rows:
            sample = rows[0]
            print(f'Sample ID: {sample.get("Person_ID")}')
            print(f'Sample Email: {sample.get("Email")}')
            print(f'Sample Password exists: {bool(sample.get("Password"))}')
else:
    print('CSV file not found')