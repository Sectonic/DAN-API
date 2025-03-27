from flask import Blueprint, request, jsonify
from app.services.auth import exchange_oauth_code, generate_response
from app.services.user import get_user, get_if_caregiver
from firebase_admin.auth import UserNotFoundError

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["GET"])
def google():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Code is required"}), 422
    
    token = exchange_oauth_code(code, provider="google")
    if not token:
        return jsonify({"error": "ID token missing"}), 401
    
    return generate_response(token, provider="google")
    
@bp.route("/whoop", methods=["GET"])
def whoop():
    code = request.args.get("code")
    state = request.args.get("state")
    if not code:
        return jsonify({"error": "Code is required"}), 422
    
    try:
        caregiver = get_user(state)
        if not get_if_caregiver(caregiver):
            return jsonify({"error": "State provided is not associated with a caregiver"}), 403
    except UserNotFoundError:
        return jsonify({"error": "State provided has no associated user"}), 404
    
    token = exchange_oauth_code(code, provider="whoop")
    if not token:
        return jsonify({"error": "ID token missing"}), 401
    
    return generate_response(token, provider="whoop")