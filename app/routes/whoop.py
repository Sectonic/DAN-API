from flask import Blueprint, request, jsonify
from app.services.whoop import WhoopService, WhoopWebhookData

bp = Blueprint("whoop", __name__)

@bp.route("/webhook", methods=["POST"])
def webhook():
    raw_body = request.get_data()
    signature_header = request.headers.get('X-WHOOP-Signature')
    timestamp_header = request.headers.get('X-WHOOP-Signature-Timestamp')
    
    valid_signature = WhoopService.validate_webhook_signature(
        raw_body, 
        signature_header, 
        timestamp_header
    )
    if valid_signature:
        return jsonify({"error": "Invalid signature"}), 403
    
    webhook_data: WhoopWebhookData  = request.json
    if not webhook_data:
        return jsonify({"error": "No webhook data provided"}), 400
    
    event_type = webhook_data["type"]
    
    try:
        if event_type.startswith('workout'):
            WhoopService.process_workout_event(webhook_data)
        elif event_type.startswith('sleep'):
            WhoopService.process_sleep_event(webhook_data)
        elif event_type.startswith('recovery'):
            WhoopService.process_recovery_event(webhook_data)
        else:
            return jsonify({"error": f"Unhandled event type: {event_type}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error processing webhook {event_type}: {str(e)}"}), 500

    return jsonify({"status": "success"}), 200
