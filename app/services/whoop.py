import requests
import hashlib
from app.types.whoop import WhoopUser, CycleScore, Cycle, SleepScore, Sleep, RecoveryScore, Recovery, ZoneDuration, WorkoutScore, Workout

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
