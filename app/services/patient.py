from firebase_admin.auth import UserRecord
from firebase_admin import firestore
from app.utils.firebase import db, auth
from typing import Optional, List, Dict
from app.services.auth import AuthService

class PatientService:
    @staticmethod
    def get_patient(uid: str) -> UserRecord:
        return AuthService.get_user(uid, 'patient')

    @staticmethod
    def create_patient(name: str) -> str:
        user_record = auth.create_user(
            display_name=name
        )
        return user_record.uid

    @staticmethod
    def get_caregiver_uid(patient_uid: str) -> Optional[str]:
        pairings = db.collection('pairings').stream()
        for pairing in pairings:
            patient_uids = pairing.to_dict().get('patient_uids', [])
            if patient_uid in patient_uids:
                return pairing.id
        return None

    @staticmethod
    def get_patient_tracks(patient_uid: str) -> List[Dict]:
        tracks_ref = db.collection('patient_data').document(patient_uid).collection('tracks')
        track_docs = tracks_ref.stream()

        track_data = []
        for doc in track_docs:
            track_data.append({
                'track_id': doc.to_dict().get('track_id', ''),
                'description': doc.to_dict().get('description', '')
            })
        return track_data
