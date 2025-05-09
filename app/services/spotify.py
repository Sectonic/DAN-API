import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import requests
from app.utils.firebase import db

class SpotifyService:
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_API_BASE = 'https://api.spotify.com/v1'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, caregiver_uid: str):
        self.caregiver_uid = caregiver_uid
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        self._load_tokens()

    def _load_tokens(self) -> None:
        doc = db.collection('giver_data').document(self.caregiver_uid).get()
        if doc.exists:
            data = doc.to_dict()
            self._access_token = data.get('spotify_access_token')
            self._refresh_token = data.get('spotify_refresh_token')
            expires_at = data.get('spotify_token_expires_at')
            self._token_expires_at = datetime.fromisoformat(expires_at)

    def _save_tokens(self, access_token: str, refresh_token: str, expires_in: int) -> None:
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        db.collection('giver_data').document(self.caregiver_uid).set({
            'spotify_access_token': access_token,
            'spotify_refresh_token': refresh_token,
            'spotify_token_expires_at': expires_at.isoformat()
        }, merge=True)
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._token_expires_at = expires_at

    def _ensure_valid_token(self) -> None:
        if not self._access_token or not self._refresh_token or not self._token_expires_at:
            raise ValueError("Please connect your Spotify account for this feature.")

        if not self._token_expires_at or datetime.now() >= self._token_expires_at:
            self._refresh_access_token()

    def _refresh_access_token(self) -> None:
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        }
        
        response = requests.post(self.TOKEN_URL, data=payload)
        response.raise_for_status()
        
        token_info = response.json()
        new_access_token = token_info.get('access_token')
        new_refresh_token = token_info.get('refresh_token', self._refresh_token)
        expires_in = token_info.get('expires_in', 3600)

        if not new_access_token:
            raise ValueError("Failed to refresh access token")
        
        self._save_tokens(new_access_token, new_refresh_token, expires_in)

    def search_tracks(self, query: str) -> List[Dict]:
        self._ensure_valid_token()
        
        url = f"{self.SPOTIFY_API_BASE}/search"
        params = {
            'q': query,
            'type': 'track',
            'limit': 5
        }
        headers = {'Authorization': f'Bearer {self._access_token}'}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get('tracks', {}).get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching tracks from Spotify: {e}")
            return []

    def get_track(self, track_id: str) -> Optional[Dict]:
        self._ensure_valid_token()
        
        url = f"{self.SPOTIFY_API_BASE}/tracks/{track_id}"
        headers = {'Authorization': f'Bearer {self._access_token}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching track from Spotify: {e}")
            return None

    def get_tracks(self, track_ids: List[str]) -> List[Dict]:
        self._ensure_valid_token()
        
        if not track_ids:
            return []
            
        tracks = []
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i + 50]
            url = f"{self.SPOTIFY_API_BASE}/tracks"
            params = {'ids': ','.join(batch)}
            headers = {'Authorization': f'Bearer {self._access_token}'}
            
            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                tracks.extend(data.get('tracks', []))
            except requests.exceptions.RequestException as e:
                print(f"Error fetching tracks from Spotify: {e}")
                continue
                
        return tracks

    @staticmethod
    def set_spotify_tokens(uid: str, access_token: str, refresh_token: str, expires_in: int = 3600) -> None:
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        db.collection('giver_data').document(uid).set({
            'spotify_access_token': access_token,
            'spotify_refresh_token': refresh_token,
            'spotify_token_expires_at': expires_at.isoformat()
        }, merge=True)

