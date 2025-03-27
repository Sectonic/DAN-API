from firebase_admin import auth
from app.utils.firebase import firebase_app

def get_user(uid: str) -> auth.UserRecord:
    return auth.get_user(uid, firebase_app)