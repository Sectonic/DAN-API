from flask import Blueprint, request, jsonify
from app.routes import fb_admin
from firebase_admin import auth
import os
import requests

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["POST", "GET"])
def google():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Code is required"}), 400
    
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
        return jsonify({'error': 'ID token missing'}), 400

    try:
        return f'<script>window.location.replace("expexp://10.91.84.194:808/auth?id_token={id_token}")</script>', 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 400