import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import HTTPException
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


# Ensure Firebase is initialized only once
if not firebase_admin._apps:
    firebase_cred_json = os.getenv('FIREBASECREDENTIALS')
    if firebase_cred_json is not None:
        firebase_creds_dict = json.loads(firebase_cred_json)
    else:
        raise ValueError(
            "Firebase credentials JSON is missing or not set properly.")

    cred = credentials.Certificate(firebase_creds_dict)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Authentication (Admin SDK does not use 'getAuth' like the JS SDK)
auth = firebase_admin.auth


async def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
