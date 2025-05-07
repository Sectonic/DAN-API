from flask import Flask
from app.routes.auth import bp as authBP
from app.routes.wondering import bp as wonderingBP
from app.routes.user import bp as userBP

def create_app():
    app = Flask(__name__)

    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(wonderingBP, url_prefix="/wondering")
    app.register_blueprint(userBP, url_prefix="/user")

    return app
