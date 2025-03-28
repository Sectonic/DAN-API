from flask import Blueprint, jsonify
from firebase_admin.auth import UserNotFoundError
from app.services.user import UserService

bp = Blueprint('user', __name__)

@bp.route('/<uid>', methods=['GET'])
def get_user(uid):
    try:
        caregiver = UserService.get_if_caregiver(UserService.get_user(uid))
        if caregiver:
            return jsonify({ "contains": True }), 200
        else:
            return jsonify({ "contains": False}), 400
    except UserNotFoundError:
        return jsonify({"contains": False}), 404
    except Exception as e:
        return jsonify({"contains": False, "error": str(e)}), 500