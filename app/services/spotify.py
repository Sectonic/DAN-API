import os
from dotenv import load_dotenv
import requests
from typing import Optional, Tuple
from app.utils.firebase import db
from app.services.auth import AuthService

load_dotenv()

class SpotifyService:
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    @staticmethod
    def set_spotify_tokens(uid: str, access_token: str, refresh_token: str) -> None:
        db.collection('giver_data').document(uid).set({
            'spotify_access_token': access_token,
            'spotify_refresh_token': refresh_token
        }, merge=True)

    @staticmethod
    def refresh_spotify_token(uid: str, refresh_token: str) -> Optional[Tuple[str, str]]:
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': SpotifyService.CLIENT_ID,
            'client_secret': SpotifyService.CLIENT_SECRET,
        }
        
        response = requests.post(AuthService.TOKEN_URLS['spotify'], data=payload)
        response.raise_for_status()
        
        token_info = response.json()
        new_access_token = token_info.get('access_token')
        new_refresh_token = token_info.get('refresh_token', refresh_token) 

        if not new_access_token:
            return None
        
        SpotifyService.set_spotify_tokens(uid, new_access_token, new_refresh_token)
        return new_access_token, new_refresh_token

