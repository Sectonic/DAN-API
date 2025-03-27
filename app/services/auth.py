import os
from dotenv import load_dotenv
import requests
from flask import jsonify
from typing import Union
from flask import Response
from typing import Optional

load_dotenv()

class AuthService:
    @staticmethod
    def exchange_oauth_code(code: str, provider: str) -> Optional[str]:
        """Exchange authorization code for token from OAuth provider"""

        token_urls = {
            'google': 'https://oauth2.googleapis.com/token',
            'whoop': 'https://api.prod.whoop.com/oauth/oauth2/token'
        }
        
        if provider not in token_urls:
            return None
        
        data = {
            'code': code,
            'client_id': os.getenv(f'{provider.upper()}_CLIENT_ID'),
            'client_secret': os.getenv(f'{provider.upper()}_CLIENT_SECRET'),
            'redirect_uri': f'https://dan-api.vercel.app/auth/{provider}',
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_urls[provider], data=data)
        tokens = response.json()
        return tokens

    @staticmethod
    def generate_response(token: str, provider: str) -> Union[str, Response]:
        """Generate redirect response with token"""
        
        try:
            route = "auth" if provider == "google" else "qr"
            token_type = "idToken" if provider == "google" else "accessToken"
            return f'<script>window.location.replace("exp://10.91.84.194:8081/{route}?{token_type}={token}")</script>', 200, {'Content-Type': 'text/html'}
        except Exception as e:
            return jsonify({"error": "Invalid token", "details": str(e)}), 400
