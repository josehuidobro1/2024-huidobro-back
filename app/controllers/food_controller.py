from app.service.food_service import create_food, foods, food_by_id
from app.models.food import Food
import re
from fastapi import HTTPException


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
            status_code=400, detail=f"{label} must be grater or equal than {minimo} ")


def validate_food(food: Food):
    validate_name(food.name, 'Name')
    validate_name(food.measure, 'Measure')
    validate_limit(food.calories_portion, 0, 'calories_portion')
    validate_limit(food.amount_carbs, 0, 'amount_carbs')
    validate_limit(food.amount_sodium, 0, 'amount_sodium')
    validate_limit(food.amount_fat, 0, 'amount_fat')
    validate_limit(food.amount_protein, 0, 'amount_protein')


def register_new_food(food: Food):
    validate_food(food)
    response = create_food(food.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "food registered successfully", "food_id": response["id"]}


def get_foods():
    response = foods()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def validate_existance(items, itemSearch, id, label):
    existing_ids = [item[itemSearch]
                    for item in items]
    if id not in existing_ids:
        raise HTTPException(
            status_code=400, detail=f"Invalid {label} ID: {id}")


def get_food_by_id(food_id: str):

    foods_created = get_foods()
    validate_existance(foods_created['message']['food'], 'id', food_id, 'food')
    response = food_by_id(food_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
