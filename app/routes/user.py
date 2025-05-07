from flask import Blueprint, jsonify
from firebase_admin.auth import UserNotFoundError
from app.services.user import UserService

bp = Blueprint('user', __name__)

@bp.route('/<uid>', methods=['GET'])
def get_caregiver(uid):
    try:
        caregiver = UserService.get_user(uid)
        if UserService.is_caregiver(caregiver):
            return jsonify({"contains": True}), 200
        else:
            return jsonify({"error": "UID is not a caregiver"}), 400
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<uid>/patients', methods=['GET'])
def get_caregiver_patients(uid):
    try:
        caregiver = UserService.get_user(uid)
        if not UserService.is_caregiver(caregiver):
            return jsonify({"error": "User is not a caregiver"}), 403
        patient_uids = UserService.get_patient_uids_for_caregiver(caregiver.uid)
        if not patient_uids:
            return jsonify({"patients": []}), 200
        patients = [UserService.get_user(patient_uid)._data for patient_uid in patient_uids]
        return jsonify({"patients": patients}), 200
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500