import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("DEBUG", True)
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "path/to/firebase/credentials.json")
