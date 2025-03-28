from typing import TypedDict, Optional
import requests
import hashlib
import hmac
import base64
from dotenv import load_dotenv
import os

load_dotenv()

class WhoopUser(TypedDict):
    user_id: str
    email: str
    first_name: str
    last_name: str
    generated_password: str

class WhoopWebhookData(TypedDict):
    user_id: int
    id: int
    type: str
    trace_id: str

class WhoopService:
    @staticmethod
    def get_user_data(token: str) -> WhoopUser:
        url = "https://api.prod.whoop.com/developer/v1/user/profile/basic"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        data["user_id"] = str(data["user_id"])
        data["generated_password"] = hashlib.sha256(data["user_id"].encode()).hexdigest()
        return data
        
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
    def process_workout_event(data: WhoopWebhookData) -> None:
        if data["type"] == "workout.updated":
            print(f"Processing workout update for user {data['user_id']}, workout {data['id']}")
        elif data["type"] == "workout.deleted":
            print(f"Processing workout deletion for user {data['user_id']}, workout {data['id']}")

    @staticmethod
    def process_sleep_event(data: WhoopWebhookData) -> None:
        if data["type"] == "sleep.updated":
            print(f"Processing sleep update for user {data['user_id']}, sleep {data['id']}")
        elif data["type"] == "sleep.deleted":
            print(f"Processing sleep deletion for user {data['user_id']}, sleep {data['id']}")

    @staticmethod
    def process_recovery_event(data: WhoopWebhookData) -> None:
        if data["type"] == "recovery.updated":
            print(f"Processing recovery update for user {data['user_id']}, recovery {data['id']}")
        elif data["type"] == "recovery.deleted":
            print(f"Processing recovery deletion for user {data['user_id']}, recovery {data['id']}")
