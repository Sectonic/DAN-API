from flask import Blueprint, request, jsonify
from app.services.auth import exchange_google_code, generate_google_response

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["GET"])
def google():
    code = request.args.get("code")
    state = request.args.get("state")
    if not code:
        return jsonify({"error": "Code is required"}), 400
    if state not in ["mobile", "desktop"]:
        return jsonify({"error": "Invalid or missing state"}), 400
    
    id_token = exchange_google_code(code)
    if not id_token:
        return jsonify({'error': 'ID token missing'}), 400
    
    return generate_google_response(state, id_token)
    
@bp.route("/whoop", methods=["GET"])
def whoop():
    return None