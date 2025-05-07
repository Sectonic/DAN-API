from firebase_admin.auth import UserRecord
from firebase_admin import firestore
from app.utils.firebase import db, auth
from app.services.auth import AuthService

class UserService:
    @staticmethod
    def get_user(uid: str) -> UserRecord:
        return auth.get_user(uid)

    @staticmethod
    def is_caregiver(user: UserRecord) -> bool:
        return any(provider.provider_id == 'google.com' for provider in user.provider_data)

    @staticmethod
    def get_pairing(uid: str) -> str | None:
        pairing_doc = db.collection('pairings').document(uid).get()
        if pairing_doc.exists:
            return pairing_doc.to_dict().get('patient_uid')
        return None

    @staticmethod
    def get_patient_uids_for_caregiver(uid: str) -> list[str] | None:
        pairing_doc = db.collection('pairings').document(uid).get()
        if pairing_doc.exists:
            return pairing_doc.to_dict().get('patient_uids', [])
        return None

    @staticmethod
    def create_patient(name: str) -> tuple[str, str]:
        user_record = auth.create_user(
            display_name=name
        )
        return user_record.uid

    @staticmethod
    def connect_users(giver_uid: str, patient_uid: str) -> None:
        pairing_ref = db.collection('pairings').document(giver_uid)
        pairing_ref.set({
            'patient_uids': firestore.ArrayUnion([patient_uid])
        }, merge=True)


