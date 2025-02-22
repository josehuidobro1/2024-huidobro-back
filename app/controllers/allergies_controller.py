from app.service.allergies_service import get_allergie, allergies, post_allergie, put_allergie
from app.models.allergies import Allergies
from app.controllers.food_controller import get_foods
from fastapi import HTTPException
import re


def validate_name(campo, label):
    if not campo.strip():
        raise HTTPException(
            status_code=400, detail=f"{label} cannot be empty or blank")
    if type(campo) is not str:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a string")
    if not re.match(r'^[a-zA-Z\s]+$', campo):
        raise HTTPException(
            status_code=400, detail=f"Invalid format for {label}. Only letters and spaces allowed.")


def validate_allergie(allergie: Allergies):
    validate_name(allergie.name, 'name')
    foods = get_foods()
    existing_food_ids = [food["id"]
                         for food in foods["message"]['food']]
    for food in allergie.foods_ids:
        if food not in existing_food_ids:
            raise HTTPException(
                status_code=400, detail=f"Invalid food ID: {food}")
    if not allergie.foods_ids:
        raise HTTPException(
            status_code=400, detail=f"The allergie must have at leat one item")


def get_allergies():
    response = allergies()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def allergieLog(allergie: Allergies):
    validate_allergie(allergie)
    allergies = get_allergies()
    existing_allergies = [aller["name"]
                          for aller in allergies["message"]['allergies']]
    if allergie.name in existing_allergies:
        raise HTTPException(
            status_code=400, detail=f"That allergy name has already exist ")
    response = post_allergie(allergie.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "allergie registered successfully", "allergie_id": response["id"]}


def updateAllergie(allergie_id: str, EditAllergie: Allergies):
    allergie = get_allergie(allergie_id)
    if not allergie['allergie']:
        raise HTTPException(
            status_code=400, detail=f"The allergie ID is not valid")
    if allergie['allergie']['name'] != EditAllergie.name:
        raise HTTPException(
            status_code=400, detail=f" You can not change allergie name  ")

    validate_allergie(EditAllergie)
    response = put_allergie(allergie_id, EditAllergie)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
