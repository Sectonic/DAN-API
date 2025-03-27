from flask import Blueprint, jsonify
from firebase_admin import auth
from app.services.user import get_user

bp = Blueprint('user', __name__)

@bp.route('/<uid>', methods=['GET'])
def get_caregiver_user(uid):
    try:
        user = get_user(uid)
        if user.provider_id != 'google.com':
            return jsonify({"contains": False}), 400
        return jsonify({"contains": True}), 200
    except auth.UserNotFoundError:
        return jsonify({"contains": False}), 404
    except Exception as e:
        return jsonify({"contains": False, "error": str(e)}), 500