import os
from dotenv import load_dotenv
import requests
from flask import jsonify
from typing import Union, Optional, Dict, Literal
from flask import Response
from app.utils.firebase import auth
from urllib.parse import urlencode
from firebase_admin.auth import UserRecord

load_dotenv()

class AuthService:

    TOKEN_URLS: Dict[str, str] = {
        'google': 'https://oauth2.googleapis.com/token',
        'spotify': 'https://accounts.spotify.com/api/token'
    }

    REDIRECT_ROUTES: Dict[str, str] = {
        'google': 'auth',
        'spotify': 'settings'
    }

    def __init__(self, url: str, provider: str):
        self.url = url;
        self.provider = provider;

    @staticmethod
    def get_user(uid: str, user_type: Literal['patient', 'caregiver']) -> UserRecord:
        user = auth.get_user(uid)
        is_caregiver = user.email is not None
        
        if user_type == 'caregiver' and not is_caregiver:
            raise ValueError("User is not a caregiver")
        elif user_type == 'patient' and is_caregiver:
            raise ValueError("User is a caregiver, not a patient")
            
        return user

    def exchange_oauth_code(self, code: str) -> Optional[Dict[str, str]]:
        if self.provider not in AuthService.TOKEN_URLS:
            return None
        
        data = {
            'code': code,
            'client_id': os.getenv(f'{self.provider.upper()}_CLIENT_ID'),
            'client_secret': os.getenv(f'{self.provider.upper()}_CLIENT_SECRET'),
            'redirect_uri': f'{os.getenv('API_BASE')}/auth/{self.provider}',
            'grant_type': 'authorization_code'
        }

        response = requests.post(AuthService.TOKEN_URLS[self.provider], data=data)
        response.raise_for_status()
        tokens = response.json()
        return tokens

    def generate_response(self, query_dict: dict[str, str] = {}) -> Union[str, Response]:
        route = AuthService.REDIRECT_ROUTES.get(self.provider)
        if not route:
            return jsonify({"error": f"Invalid provider specified: {self.provider}"}), 400
        query = urlencode(query_dict)
        redirect_url = f"{self.url}/{route}?{query}"
        return f'<script>window.location.replace("{redirect_url}")</script>', 200, {'Content-Type': 'text/html'}

    @staticmethod
    def generate_patient_token(patient_uid: str, caregiver_uid: str) -> str:
        custom_token = auth.create_custom_token(patient_uid, {"caregiver_uid": caregiver_uid})
        return custom_token.decode('utf-8')