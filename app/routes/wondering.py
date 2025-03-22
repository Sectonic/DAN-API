from flask import Blueprint, request, jsonify
from app.services import track_location

bp = Blueprint("wondering", __name__)

@bp.route("/track", methods=["POST"])
def track():
    data = request.json
    return jsonify(track_location(data))
