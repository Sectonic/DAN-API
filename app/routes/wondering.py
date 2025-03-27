from flask import Blueprint, jsonify

bp = Blueprint("wondering", __name__)

@bp.route("/track", methods=["POST"])
def track():
    return jsonify({ 'message': 'Tracking endpoint is under development' })
