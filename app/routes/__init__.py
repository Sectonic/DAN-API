import firebase_admin
import os

firebase_admin.initialize_app(options={
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
})

from .auth import bp as auth
from .wondering import bp as wondering
from .whoop import bp as whoop
