from flask import Blueprint, jsonify
from firebase_admin.auth import UserNotFoundError
from app.services.caregiver import CaregiverService
from app.services.auth import AuthService

bp = Blueprint('caregiver', __name__)

@bp.route('/<uid>/patients', methods=['GET'])
def get_caregiver_patients(uid):
    try:
        caregiver = AuthService.get_user(uid, 'caregiver')
        patient_uids = CaregiverService.get_patient_uids(caregiver.uid)
        if not patient_uids:
            return jsonify({"patients": []}), 200
        patients = [AuthService.get_user(patient_uid, 'patient')._data for patient_uid in patient_uids]
        return jsonify({"patients": patients}), 200
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500