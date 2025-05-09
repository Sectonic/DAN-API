from flask import Blueprint, jsonify, request
from app.services.patient import PatientService
from app.services.spotify import SpotifyService
from app.services.auth import AuthService
from firebase_admin.auth import UserNotFoundError

bp = Blueprint('spotify', __name__)

@bp.route('/<patient_uid>/track/<track_id>', methods=['GET'])
def get_track(patient_uid, track_id):
    try:
        AuthService.get_user(patient_uid, 'patient')
        
        caregiver_uid = PatientService.get_caregiver_uid(patient_uid)
        if not caregiver_uid:
            return jsonify({'error': 'No caregiver found for this patient'}), 404

        spotify = SpotifyService(caregiver_uid)
        track = spotify.get_track(track_id)
        if not track:
            return jsonify({'error': 'Track not found'}), 404
            
        return jsonify({'track': track})
    except UserNotFoundError:
        return jsonify({'error': 'User not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<patient_uid>/search', methods=['GET'])
def search_tracks(patient_uid):
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400

        AuthService.get_user(patient_uid, 'patient')
        
        caregiver_uid = PatientService.get_caregiver_uid(patient_uid)
        if not caregiver_uid:
            return jsonify({'error': 'No caregiver found for this patient'}), 404

        spotify = SpotifyService(caregiver_uid)
        results = spotify.search_tracks(query)
        
        return jsonify({'tracks': results})
    except UserNotFoundError:
        return jsonify({'error': 'User not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500
