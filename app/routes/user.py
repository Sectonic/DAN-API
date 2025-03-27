from flask import Blueprint, jsonify
from firebase_admin import auth
from app.services.user import get_user, get_if_caregiver

bp = Blueprint('user', __name__)

@bp.route('/<uid>', methods=['GET'])
def get_caregiver_user(uid):
    try:
        caregiver = get_if_caregiver(get_user(uid))
        return (jsonify({ "contains": True }), 200) if caregiver else (jsonify({ "contains": False}), 400)
    except auth.UserNotFoundError:
        return jsonify({"contains": False}), 404
    except Exception as e:
        return jsonify({"contains": False, "error": str(e)}), 500