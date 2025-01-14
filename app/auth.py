from firebase_admin import auth

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']
        return user_id
    except Exception as e:
        return None
