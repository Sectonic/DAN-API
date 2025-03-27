from firebase_admin import auth
from app.utils.firebase import firebase_app
from app.services.whoop import WhoopUser

class UserService:
    @staticmethod
    def get_user(uid: str) -> auth.UserRecord:
        return auth.get_user(uid, firebase_app)
    
    @staticmethod
    def get_if_caregiver(user: auth.UserRecord) -> bool:
        return user.provider_data[0].provider_id == 'google.com'
    
    @staticmethod
    def create_user(data: WhoopUser):
        user = auth.create_user(
            uid=data['user_id'],
            display_name=f'{data["first_name"]} ${data["last_name"]}',
            email=data['email'],
            email_verified=True,
            password=f'WHOOP${data['user_id']}'
        )
