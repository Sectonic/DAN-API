from firebase_admin.auth import UserRecord
from app.utils.firebase import db, auth
from app.services.whoop import WhoopUser

class UserService:
    @staticmethod
    def get_user(uid: str) -> UserRecord:
        return auth.get_user(uid)
    
    @staticmethod
    def get_if_caregiver(user: UserRecord) -> bool:
        return user.provider_data[0].provider_id == 'google.com'
    
    @staticmethod
    def get_if_connected(uid: str) -> bool:
        giver_query = db.collection('pairings').where('giver_uid', '==', uid).limit(1).get()
        return len(list(giver_query)) > 0
    
    @staticmethod
    def create_user(data: WhoopUser) -> None:
        auth.create_user(
            uid=data['user_id'],
            display_name=f'{data["first_name"]} ${data["last_name"]}',
            email=data['email'],
            email_verified=True,
            password=data['generated_password'],
        )
    
    @staticmethod 
    def update_user(data: WhoopUser) -> None:
        auth.update_user(data['user_id'],
            display_name=f'{data["first_name"]} ${data["last_name"]}',
            email=data['email'], 
        )
    
    @staticmethod
    def connect_users(giver_uid: str, receiver_uid: str) -> None:
        db.collection('pairings').add({
            'giver_uid': giver_uid,
            'receiver_uid': receiver_uid,
        })


