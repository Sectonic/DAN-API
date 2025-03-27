from flask import Blueprint, jsonify, request
from app.services.wondering import WonderingService

bp = Blueprint("wondering", __name__)

@bp.route("/track", methods=["POST"])
def track():
    data = request.json
    return jsonify(WonderingService.track_location(data))
