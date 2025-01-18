from app.service.allergies_service import allergies, post_allergie, put_allergie
from app.models.allergies import Allergies
from fastapi import HTTPException


def get_allergies():
    response = allergies()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def allergieLog(allergie: Allergies):
    response = post_allergie(allergie.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "allergie registered successfully", "allergie_id": response["id"]}


def updateAllergie(allergie_id: str, EditAllergie: Allergies):
    response = put_allergie(allergie_id, EditAllergie)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
