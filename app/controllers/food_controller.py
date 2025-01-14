from app.service.food_service import create_food, foods, food_by_id
from app.models.food import Food
from fastapi import HTTPException


def register_new_food(food: Food):
    response = create_food(food.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "food registered successfully", "food_id": response["id"]}

def get_foods():
    response = foods()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def get_food_by_id(food_id: str):
    response = food_by_id(food_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}