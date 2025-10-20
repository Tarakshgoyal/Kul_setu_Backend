import requests

response = requests.get('https://kul-setu-backend.onrender.com/family-members', timeout=15)
if response.status_code == 200:
    data = response.json()
    if len(data) > 0:
        sample = data[0]
        print('Sample member keys:', list(sample.keys())[:15])
        print('Sample member (first 10 fields):')
        for key in list(sample.keys())[:10]:
            print(f'  {key}: {sample[key]}')
