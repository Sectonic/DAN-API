from flask import Blueprint, request, jsonify
from app.services import login_user, logout_user

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["POST"])
def google():
    data = request.json
    return jsonify(login_user(data))

@bp.route("/whoop", methods=["POST"])
def whoop():
    return jsonify(logout_user())
