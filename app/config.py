import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import HTTPException
import os
import json
from dotenv import load_dotenv

load_dotenv()


# Ensure Firebase is initialized only once
firebase_cred_json = os.environ.get("FIREBASECREDENTIALS")
if firebase_cred_json:
    try:
        firebase_creds_dict = json.loads(firebase_cred_json)
        cred = credentials.Certificate(firebase_creds_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in FIREBASECREDENTIALS.")
else:
    raise ValueError(
        "Firebase credentials not found in environment variables.")

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
