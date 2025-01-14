from app.service.foodUser_service import update_food_user, create_food_user_service, get_user_meals, delete_food_user_service
from app.models.userFood import UserFood
from fastapi import HTTPException
from datetime import datetime


def userFoodLog(userFood: UserFood):
    response = create_food_user_service(userFood)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully"}


def get_meals_user(user_id: str):
    response = get_user_meals(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_meal(userFood_id: str):
    response = delete_food_user_service(userFood_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])


def update_userFood_controller(userFood_id: str, userFood_data: UserFood):
    response = update_food_user(userFood_id, userFood_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
