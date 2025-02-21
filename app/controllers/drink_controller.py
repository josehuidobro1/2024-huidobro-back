from app.service.drink_service import create_drink, drinks, drink_by_id, delete_drink, update_Drink, GroupedDrinks
from app.models.drink import Drink
from app.controllers.drinkType_controller import get_drinkTypes
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


def validate_limit(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo <= campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo}")


def validate_measure(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo < campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo}")


def validate_drink(id_user: str, drink: Drink):
    if id_user != drink.id_User:
        raise HTTPException(
            status_code=400, detail=f"The id_User is not valid")
    validate_name(drink.name, "name")
    validate_name(drink.measure, "measure")
    validate_limit(drink.sugar_portion, 0, "sugar_portion")
    validate_limit(drink.caffeine_portion, 0, "caffeine_portion")
    validate_measure(drink.measure_portion, 0, "measure_portion")
    validate_limit(drink.calories_portion, 0, "calories_portion")

    drinks = get_drinkTypes()
    existing_drinksType_ids = []
    for type in drinks["message"]['drinkType']:
        if type["id_user"] in [id_user, "default"]:
            existing_drinksType_ids.append(type["id"])
    if drink.typeOfDrink not in existing_drinksType_ids:
        raise HTTPException(
            status_code=400, detail="The drink type id is not valid")


def register_new_drink(id_user: str, drink: Drink):

    validate_drink(id_user, drink)
    response = create_drink(drink.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "drink registered successfully", "drink_id": response["id"]}


def get_drinks(user_id: str):
    response = drinks(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def get_drink_by_id(user_id: str, drink_id: str):
    user_drinks = get_drinks(user_id)
    existing_drinks_ids = [drink['id']
                           for drink in user_drinks['message']['Drinks']]
    if drink_id not in existing_drinks_ids:
        raise HTTPException(
            status_code=400, detail="The drink id is not valid")
    response = drink_by_id(drink_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def deletedrink(user_id: str, drink_id: str):
    user_drinks = get_drinks(user_id)
    existing_drinks_ids = [drink['id']
                           for drink in user_drinks['message']['Drinks']]
    if drink_id not in existing_drinks_ids:
        raise HTTPException(
            status_code=400, detail="The drink id is not valid")
    response = delete_drink(drink_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])


def Updatedrink(user_id: str, drink_id: str, UpdatedData: Drink):
    user_drinks = get_drinks(user_id)
    existing_drinks_ids = [drink['id']
                           for drink in user_drinks['message']['Drinks']]
    if drink_id not in existing_drinks_ids:
        raise HTTPException(
            status_code=400, detail="The drink id is not valid")
    validate_drink(user_id, UpdatedData)
    response = update_Drink(drink_id, UpdatedData)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response


def Grouped_Drinks(drink_id: str):
    response = GroupedDrinks(drink_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
