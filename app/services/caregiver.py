from firebase_admin.auth import UserRecord
from firebase_admin import firestore
from app.utils.firebase import db, auth
from typing import Optional, List
from app.services.auth import AuthService

class CaregiverService:
    @staticmethod
    def get_caregiver(uid: str) -> UserRecord:
        return AuthService.get_user(uid, 'caregiver')

    @staticmethod
    def get_patient_uids(uid: str) -> List[str]:
        pairing_doc = db.collection('pairings').document(uid).get()
        if pairing_doc.exists:
            return pairing_doc.to_dict().get('patient_uids', [])
        return []

    @staticmethod
    def connect_patient(giver_uid: str, patient_uid: str) -> None:
        pairing_ref = db.collection('pairings').document(giver_uid)
        pairing_ref.set({
            'patient_uids': firestore.ArrayUnion([patient_uid])
        }, merge=True) 