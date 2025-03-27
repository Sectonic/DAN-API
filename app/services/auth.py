import os
import requests
from flask import jsonify

def exchange_google_code(code):
    """Exchange authorization code for token from Google OAuth"""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': 'https://dan-api.vercel.app/auth/google',
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, data=data)
    tokens = response.json()
    
    id_token = tokens.get('id_token')
    if not id_token:
        return None
        
    return id_token

def generate_google_response(state, id_token):
    """Generate redirect google response with token"""
    redirect_path = "exp://10.91.84.194:8081" if state == "mobile" else "http://localhost:8081"
    
    try:
        return f'<script>window.location.replace("{redirect_path}/auth?id_token={id_token}")</script>', 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 400
