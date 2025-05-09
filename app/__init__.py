from flask import Flask
from app.routes.auth import bp as authBP
from api.app.routes.caregiver import bp as caregiverBP
from app.routes.spotify import bp as spotifyBP
from app.routes.patient import bp as patientBP

def create_app():
    app = Flask(__name__)

    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(patientBP, url_prefix="/patient")
    app.register_blueprint(caregiverBP, url_prefix="/caregiver")
    app.register_blueprint(spotifyBP, url_prefix="/spotify")

    return app
