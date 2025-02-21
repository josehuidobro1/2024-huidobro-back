from app.service.drinkType_service import create_drinkType, drinkType, drinkType_by_id, getUserDrinkTypes, deleteDrinkType
from app.models.drinkType import DrinkType
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


def register_new_drinkType(user_id: str, drinkType: DrinkType):
    if drinkType.id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"The user id is not valid")
    validate_name(drinkType.name, "name")
    response = create_drinkType(drinkType.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "drinkType registered successfully", "drinkType_id": response["id"]}


def get_drinkTypes():
    response = drinkType()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def get_drinkType_by_id(drinkType_id: str):
    response = drinkType_by_id(drinkType_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def UserDrinkTypes(user_id: str):
    response = getUserDrinkTypes(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_DrinkType(id_user: str, drinkType_id: str):
    drink_types = UserDrinkTypes(id_user)
    existing_id = []
    for type in drink_types['message']['drinkType']:
        existing_id.append(type['id'])
    if drinkType_id not in existing_id:
        raise HTTPException(
            status_code=400, detail="The drink type ID is not valid")
    response = deleteDrinkType(drinkType_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
