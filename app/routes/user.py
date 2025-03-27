from flask import Blueprint, jsonify
from firebase_admin import auth
from app.routes import fb_admin

bp = Blueprint('user', __name__)

@bp.route('/<uid>', methods=['GET'])
def get_user(uid):
    try:
        user = auth.get_user(uid, fb_admin)
        if user:
            return jsonify({"contains": True}), 200
    except auth.UserNotFoundError:
        return jsonify({"contains": False}), 404
    except Exception as e:
        return jsonify({"contains": False, "error": str(e)}), 500