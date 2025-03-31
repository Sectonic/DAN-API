from firebase_admin.auth import UserRecord
from app.utils.firebase import db, auth
from app.types.whoop import WhoopUser

class UserService:
    @staticmethod
    def get_user(uid: str) -> UserRecord:
        return auth.get_user(uid)
    
    @staticmethod
    def get_if_caregiver(user: UserRecord) -> bool:
        return user.provider_data[0].provider_id == 'google.com'
    
    @staticmethod
    def get_if_connected(uid: str) -> bool:
        giver_query = db.collection('pairings').document(uid).get()
        return giver_query.exists
    
    @staticmethod
    def create_user(data: WhoopUser, access_token: str, refresh_token: str) -> None:
        auth.create_user(
            uid=data['user_id'],
            display_name=f'{data["first_name"]} ${data["last_name"]}',
            email=data['email'],
            email_verified=True,
            password=data['generated_password'],
        )
        db.collection('receiver_data').document(data['user_id']).set({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    
    @staticmethod 
    def update_user(data: WhoopUser, access_token: str, refresh_token: str) -> None:
        auth.update_user(
            data['user_id'],
            display_name=f'{data["first_name"]} ${data["last_name"]}',
            email=data['email'], 
        )
        db.collection('receiver_data').document(data['user_id']).set({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    
    @staticmethod
    def connect_users(giver_uid: str, receiver_uid: str) -> None:
        db.collection('pairings').document(giver_uid).set({
            'receiver_uid': receiver_uid,
        })


