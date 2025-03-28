from flask import Blueprint, request, jsonify
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.whoop import WhoopService
from firebase_admin.auth import UserNotFoundError

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["GET"])
def google():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Code is required"}), 422
    
    tokens = AuthService.exchange_oauth_code(code, provider="google")
    id_token = tokens.get('id_token')
    if not id_token:
        return jsonify({"error": "ID token missing"}), 401
    
    return AuthService.generate_response({ 
        "id_token": id_token 
    }, provider="google")
    
@bp.route("/whoop", methods=["GET"])
def whoop():
    code = request.args.get("code")
    state = request.args.get("state")
    if not code:
        return jsonify({"error": "Code is required"}), 422
    
    try:
        caregiver = UserService.get_user(state)
        if not UserService.get_if_caregiver(caregiver):
            return jsonify({"error": "State provided is not associated with a caregiver"}), 403
    except UserNotFoundError:
        return jsonify({"error": "State provided has no associated user"}), 404
    
    tokens = AuthService.exchange_oauth_code(code, provider="whoop")
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    if not access_token or not refresh_token:
        return jsonify({"error": "Access token missing"}), 401
    
    user_data = WhoopService.get_user_data(access_token)
    try:
        UserService.get_user(user_data["user_id"])
        UserService.update_user(user_data)
    except UserNotFoundError:
        if UserService.get_if_connected(state):
            return AuthService.generate_response({
                "error": "Caregiver already has a receiver"
            }, provider="whoop");
        UserService.create_user(user_data)
        UserService.connect_users(state, user_data["user_id"])

    return AuthService.generate_response({ 
        "uid": user_data["user_id"],
        "caregiver_uid": state,
        "email": user_data["email"],
        "generated_password": user_data["generated_password"]
    }, provider="whoop")





