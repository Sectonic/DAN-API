from flask import Blueprint

bp = Blueprint("whoop", __name__)

@bp.route("/", methods=["GET"])
def index():
    return {"message": "Whoop service is running"}
