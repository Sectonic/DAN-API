from flask import Flask
from .routes import auth, wondering, whoop

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Register blueprints
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(wondering.bp, url_prefix="/wondering")
    app.register_blueprint(whoop.bp, url_prefix="/whoop")

    return app
