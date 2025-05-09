from flask import Blueprint, jsonify
from firebase_admin.auth import UserNotFoundError
from app.services.patient import PatientService
from app.services.auth import AuthService
from app.services.spotify import SpotifyService

bp = Blueprint('patient', __name__)

@bp.route('/<uid>/settings', methods=['GET'])
def get_patient_settings(uid):
    try:
        patient = AuthService.get_user(uid, 'patient')
        caregiver_uid = PatientService.get_caregiver_uid(uid)
        if not caregiver_uid:
            return jsonify({"error": "No caregiver found for patient"}), 404
        
        response = {
            "patient": patient._data,
            "tracks": []
        }
            
        track_data = PatientService.get_patient_tracks(uid)
        track_ids = [track['track_id'] for track in track_data]
        try: 
            spotify_service = SpotifyService(caregiver_uid)
            spotify_tracks = spotify_service.get_tracks(track_ids)

            for i in range(len(spotify_tracks)):
                response['tracks'].append({
                    'id': spotify_tracks[i]['id'],
                    'name': spotify_tracks[i]['name'], 
                    'artists': [artist['name'] for artist in spotify_tracks[i]['artists']],
                    'cover_image': spotify_tracks[i]['album']['images'][0]['url'] 
                        if spotify_tracks[i]['album']['images'] else None,
                    'description': track_data[i]['description']
                })
        except Exception as e:
            response['spotify_error'] = str(e)

        return jsonify(response), 200
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
