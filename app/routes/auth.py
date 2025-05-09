from flask import Blueprint, request, jsonify
from app.services.auth import AuthService
from app.services.caregiver import CaregiverService
from app.services.patient import PatientService
from app.services.spotify import SpotifyService
from firebase_admin.auth import UserNotFoundError
import json

bp = Blueprint("auth", __name__)

@bp.route("/google", methods=["GET"])
def google():
    code = request.args.get("code")
    state = request.args.get("state")
    if not all([code, state]):
        return jsonify({"error": "Missing required fields: code, state"}), 422
    
    auth = AuthService(state, "google")
    
    tokens = auth.exchange_oauth_code(code)
    id_token = tokens.get('id_token')
    if not id_token:
        return auth.generate_response({"error": "ID token missing"})
    
    return auth.generate_response({"id_token": id_token})

@bp.route("/spotify", methods=["GET"])
def spotify():
    code = request.args.get("code")
    state = request.args.get("state")
    if not all([code, state]):
        return jsonify({"error": "Missing required fields: code, state"}), 422

    try:
        state = json.loads(state)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid state format: Not valid JSON"}), 400
    
    if 'url' not in state or 'uid' not in state:
        return jsonify({"error": "Invalid state format: Missing 'url' or 'uid' key"}), 400
    
    auth = AuthService(state['url'], 'spotify')
    
    tokens = auth.exchange_oauth_code(code)
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    if not all([access_token, refresh_token]):
        return auth.generate_response({"error": "Missing tokens: access token, refresh token"})
    
    SpotifyService.set_spotify_tokens(state['uid'], access_token, refresh_token)
    return auth.generate_response()

@bp.route("/patient/create", methods=["POST"])
def patient_create():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    name = data.get("name")
    caregiver_uid = data.get("caregiver_uid")

    if not all([name, caregiver_uid]):
        print(name, caregiver_uid)
        return jsonify({"error": "Missing required fields: name, caregiver_uid"}), 422
    
    try:
        AuthService.get_user(caregiver_uid, 'caregiver')
    except UserNotFoundError:
        return jsonify({"error": "Provided caregiver_uid has no associated user"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
         return jsonify({"error": f"Error validating caregiver: {str(e)}"}), 500

    try:
        patient_uid = PatientService.create_patient(name)
        CaregiverService.connect_patient(caregiver_uid, patient_uid)
        custom_token = AuthService.generate_patient_token(patient_uid, caregiver_uid)
        return jsonify({"custom_token": custom_token}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create patient: {str(e)}"}), 500

@bp.route("/patient/login", methods=["POST"])
def patient_login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    caregiver_uid = data.get("caregiver_uid")
    patient_uid = data.get("patient_uid")

    if not all([caregiver_uid, patient_uid]):
        return jsonify({"error": "Missing required fields: caregiver_uid, patient_uid"}), 422

    try:
        AuthService.get_user(caregiver_uid, 'caregiver')
        AuthService.get_user(patient_uid, 'patient')
    except UserNotFoundError:
        return jsonify({"error": "Provided caregiver_uid or patient_uid has no associated user"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
         return jsonify({"error": f"Error validating users: {str(e)}"}), 500

    associated_patient_uids = CaregiverService.get_patient_uids(caregiver_uid)
    if patient_uid not in associated_patient_uids:
        return jsonify({"error": "Patient is not associated with this caregiver"}), 403

    try:
        custom_token = AuthService.generate_patient_token(patient_uid, caregiver_uid)
        return jsonify({"custom_token": custom_token}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate patient token: {str(e)}"}), 500



