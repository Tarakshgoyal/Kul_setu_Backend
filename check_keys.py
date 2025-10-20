import requests

response = requests.get('https://kul-setu-backend.onrender.com/family-members', timeout=15)
if response.status_code == 200:
    data = response.json()
    if len(data) > 0:
        sample = data[0]
        print('Person ID:', sample.get('person_id'))
        print('First Name:', sample.get('first_name'))
        print('Email:', sample.get('email'))
        print('Password exists:', bool(sample.get('password')))
        print('Family Line ID:', sample.get('family_line_id'))
        print()
        print('Total fields in member:', len(sample))
        print('All keys:', list(sample.keys()))
