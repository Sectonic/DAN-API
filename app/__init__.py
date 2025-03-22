from flask import Flask
from .routes.auth import bp as authBP
from .routes.wondering import bp as wonderingBP
from .routes.whoop import bp as whoopBP

def create_app():
    app = Flask(__name__)

    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(wonderingBP, url_prefix="/wondering")
    app.register_blueprint(whoopBP, url_prefix="/whoop")

    return app
