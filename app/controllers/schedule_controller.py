from app.service.schedule_service import update_schedule_user, user_schedule, get_user_schedule, delete_schedule_user
from app.models.schedule import Schedule
from app.controllers.food_controller import get_foods
from fastapi import HTTPException
from app.service.plate_service import get_plates
from app.service.drink_service import drinks
import re

days = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]


def validate_limit(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo <= campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo}")


def validate_schedule(id_user: str, schedule: Schedule):
    foods = get_foods()
    existing_food_ids = [food["id"]
                         for food in foods["message"]['food']]
    user_drinks = drinks(id_user)
    existing_drinks_ids = [drink["id"] for drink in user_drinks['Drinks']]
    plates = get_plates()
    existing_plate_ids = [plate["id"] for plate in plates]
    existind_ids = existing_food_ids+existing_drinks_ids+existing_plate_ids
    for food in schedule.foodList:
        if food.food_id not in existind_ids:
            raise HTTPException(
                status_code=400, detail=f"the food ID {food.food_id} is not valid ")
        validate_limit(food.quantity, 0,
                       f" The quantity of food ID {food.food_id}")
    if schedule.day not in days:
        raise HTTPException(
            status_code=400, detail=f" The day is not valid ")


def scheduleLog(schedule: Schedule):
    days_register = [item['day']
                     for item in get_schedule_user(schedule.id_user)["message"]["schedules"]]
    if schedule.day in days_register:
        raise HTTPException(
            status_code=400, detail=f"It already exist a schedule for that day ")

    if len(schedule.foodList) == 0:
        raise HTTPException(
            status_code=400, detail=f" The food list is empty ")
    validate_schedule(schedule.id_user, schedule)
    response = user_schedule(schedule)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Schedule registered successfully"}


def get_schedule_user(user_id: str):
    response = get_user_schedule(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_schedule(user_id: str):
    response = delete_schedule_user(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])


def update_schedule(id: str, schedule_data: Schedule):
    schedule_exist = [item['id']
                      for item in get_schedule_user(schedule_data.id_user)["message"]["schedules"]]
    if id not in schedule_exist:
        raise HTTPException(
            status_code=400, detail=f" The schedule ID is not valid ")
    validate_schedule(schedule_data.id_user, schedule_data)
    response = update_schedule_user(id, schedule_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
