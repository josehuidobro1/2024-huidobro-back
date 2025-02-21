from app.service.allergies_service import allergies, post_allergie, put_allergie
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
    allergies = get_allergies()
    print(allergies)
    existing_allergies = [aller["name"]
                          for aller in allergies["message"]['allergies']]
    if allergie.name in existing_allergies:
        raise HTTPException(
            status_code=400, detail=f"That allergy name has already exist ")
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
    response = post_allergie(allergie.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "allergie registered successfully", "allergie_id": response["id"]}


def updateAllergie(allergie_id: str, EditAllergie: Allergies):
    allergies = get_allergies()
    existed_all = [all['id'] for all in allergies['message']['allergie']]
    if allergie_id not in existed_all:
        raise HTTPException(
            status_code=400, detail=f"The allergie ID is not valid")
    validate_allergie(EditAllergie)
    response = put_allergie(allergie_id, EditAllergie)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
