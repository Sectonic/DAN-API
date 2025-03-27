from typing import TypedDict
import requests

class WhoopUser(TypedDict):
    user_id: int
    email: str
    first_name: str
    last_name: str

class WhoopService:
    @staticmethod
    def get_user_data(token: str) -> WhoopUser:
        url = "https://api.prod.whoop.com/developer/v1/user/profile/basic"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
