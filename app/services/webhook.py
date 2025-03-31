from typing import Optional
import hashlib
import hmac
import base64
from dotenv import load_dotenv
import os
from app.types.webhook import WebhookData
from app.utils.firebase import db

load_dotenv()

class WebhookService:
    @staticmethod
    def validate_webhook_signature(
        raw_body: bytes, 
        signature_header: Optional[str], 
        timestamp_header: Optional[str]
    ) -> bool:
        if not signature_header or not timestamp_header:
            return False

        try:
            client_secret = os.getenv("WHOOP_CLIENT_SECRET")

            message = timestamp_header.encode() + raw_body
            signature = hmac.new(
                key=client_secret.encode(),
                msg=message,
                digestmod=hashlib.sha256
            )
            calculated_signature = base64.b64encode(signature.digest()).decode()
            return hmac.compare_digest(calculated_signature, signature_header)
        except:
            return False
    
    @staticmethod
    def process_event(data: WebhookData) -> None:
        db.collection('webhook_events').add({
            'user_id': data['user_id'],
            'event_type': data['type'],
            'timestamp': data['timestamp'],
            'details': data
        })