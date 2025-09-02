from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import re


app = Flask(__name__)
CORS(app)

class FamilySearchEngine:
    def __init__(self, data_file='data.json'):
        with open(data_file, 'r') as f:
            data = json.load(f)
        self.family_members = data['mockFamilyMembers']
        self.person_map = {member['personId']: member for member in self.family_members}
        self.family_map = defaultdict(list)
        self.father_children_map = defaultdict(list)
        self.mother_children_map = defaultdict(list)
        
        for member in self.family_members:
            self.family_map[member['familyId']].append(member)
            if member.get('fatherId'):
                self.father_children_map[member['fatherId']].append(member)
            if member.get('motherId'):
                self.mother_children_map[member['motherId']].append(member)
        
        self.prepare_ml_features()
    
    def prepare_ml_features(self):
        """Prepare text features for ML-based similarity search"""
        self.text_features = []
        for member in self.family_members:
            text = f"{member.get('firstName', '')} {member.get('lastName', '')} {member.get('passion', '')} {member.get('trait', '')} {member.get('nature', '')} {member.get('about', '')}"
            self.text_features.append(text.lower())
        
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.text_features)
    
    def exact_match_search(self, query):
        """Traditional exact/partial match search"""
        results = []
        family_id = query.get('familyId')
        
        members_to_search = self.family_map[family_id] if family_id else self.family_members
        
        for member in members_to_search:
            match = True
            
            for field, value in query.items():
                if not value: 
                    continue
                    
                member_value = member.get(field)
                if member_value is None:
                    match = False
                    break
                
                if field in ['generation', 'birthYear']:
                    if int(member_value) != int(value):
                        match = False
                        break
                elif field in ['firstName', 'lastName', 'personId', 'familyId', 'bloodGroup', 'eyeColor']:
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
        query_text = ""
        for field, value in query.items():
            if value and field in ['firstName', 'lastName', 'passion', 'trait', 'nature']:
                query_text += f" {value}"
        
        if not query_text.strip():
            return []
        
        query_vector = self.vectorizer.transform([query_text.lower()])
        
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        results = []
        family_id = query.get('familyId')
        
        for i, similarity in enumerate(similarities):
            if similarity > threshold:
                member = self.family_members[i]
                if family_id and member['familyId'] != family_id:
                    continue
                member = member.copy()
                member['similarity_score'] = float(similarity)
                results.append(member)
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results
    
    def search(self, query):
        """Main search function combining exact match and ML similarity"""
        if not query:
            family_id = query.get('familyId')
            if family_id:
                return self.family_map[family_id]
            return self.family_members
        
        exact_results = self.exact_match_search(query)
        if exact_results:
            return exact_results
        
        ml_results = self.ml_similarity_search(query)
        if ml_results:
            return ml_results
        
        return []

search_engine = FamilySearchEngine()

@app.route('/search', methods=['POST'])
def search_families():
    try:
        query = request.get_json() or {}
        
        clean_query = {k: v for k, v in query.items() if v and str(v).strip()}
        
        print(f"Search Query: {clean_query}")
        
        # Perform search
        results = search_engine.search(clean_query)
        
        print(f"Found {len(results)} results")
        
        for i, result in enumerate(results[:3]):
            print(f"Result {i+1}: {result.get('firstName')} {result.get('lastName')} - {result.get('familyId')}")
            if 'similarity_score' in result:
                print(f"  Similarity Score: {result['similarity_score']:.3f}")
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Kul Setu ML Search Backend is running'})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    stats = {
        'total_members': len(search_engine.family_members),
        'total_families': len(search_engine.family_map),
        'families': {fid: len(members) for fid, members in search_engine.family_map.items()}
    }
    return jsonify(stats)

if __name__ == '__main__':
    print("Starting Kul Setu ML Search Backend...")
    print(f"Loaded {len(search_engine.family_members)} family members")
    print(f"Loaded {len(search_engine.family_map)} families")
    app.run(debug=True, host='127.0.0.1', port=5000)
