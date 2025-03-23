from flask import Blueprint, request, jsonify
from firebase_admin import auth

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["POST", "GET"])
def google():
    print(vars(request))
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        return f'<script>window.location.replace("exp://192.168.5.164:8081/auth?uid={uid}")</script>', 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 400