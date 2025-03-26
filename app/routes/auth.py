from flask import Blueprint, request, jsonify
import os
import requests

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["GET"])
def google():
    code = request.args.get("code")
    state = request.args.get("state")
    if not code:
        return jsonify({"error": "Code is required"}), 400
    if state not in ["mobile", "desktop"]:
        return jsonify({"error": "Invalid or missing state"}), 400
    redirect_path = "exp://10.91.84.194:8081" if state == "mobile" else "http://localhost:8081"
    
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
        return f'<script>window.location.replace("{redirect_path}/auth?id_token={id_token}")</script>', 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 400
    
@bp.route("/whoop", methods=["GET"])
def whoop():
    return None