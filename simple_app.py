from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register_member():
    data = request.get_json()
    print(f"Registration data received: {data}")
    
    return jsonify({
        'success': True,
        'message': 'Family member registered successfully (mock)',
        'personId': 'MOCK123',
        'familyId': 'MOCK456'
    })

@app.route('/search', methods=['POST'])
def search_families():
    query = request.get_json() or {}
    print(f"Search query: {query}")
    
    # Mock search results
    mock_results = [
        {
            'person_id': 'f1p1',
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'family_id': 'f1',
            'generation': 1,
            'birth_year': 1940,
            'blood_group': 'B+',
            'eye_color': 'Brown',
            'passion': 'Teaching',
            'trait': 'Wise',
            'nature': 'Patient',
            'about': 'Family patriarch'
        }
    ]
    
    return jsonify(mock_results)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Kul Setu Backend is running (mock mode)'})

if __name__ == '__main__':
    print("Starting Kul Setu Backend (Mock Mode)...")
    print("Registration and search endpoints available")
    app.run(debug=True, host='127.0.0.1', port=5000)