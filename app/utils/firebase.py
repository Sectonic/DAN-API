import firebase_admin
from firebase_admin import credentials, initialize_app, firestore, auth
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40dementia-assistance-network.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    })
    return initialize_app(cred)

if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
    firebase_app = firebase_admin.get_app()
else:
    firebase_app = initialize_firebase()
db = firestore.client(firebase_app)
auth = auth.Client(firebase_app)
