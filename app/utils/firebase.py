import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase(credential_path):
    cred = credentials.Certificate(credential_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()
