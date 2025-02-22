import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import HTTPException
import os
import json
from dotenv import load_dotenv

load_dotenv()


# Ensure Firebase is initialized only once
if not firebase_admin._apps:
    firebase_cred_json = os.getenv('FIREBASECREDENTIALS')
    firebase_creds_dict = json.loads(firebase_cred_json)

    cred = credentials.Certificate(firebase_creds_dict)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Authentication (Admin SDK does not use 'getAuth' like the JS SDK)
auth = firebase_admin.auth


def create_token(user_id: str) -> str:
    try:
        custom_token = auth.create_custom_token(user_id)
        return custom_token.decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating custom token {str(e)}")


def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
