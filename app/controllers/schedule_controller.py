from app.service.schedule_service import update_schedule_user, user_schedule, get_user_schedule, delete_schedule_user
from app.models.schedule import Schedule
from fastapi import HTTPException


def scheduleLog(schedule: Schedule):
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
    response = update_schedule_user(id, schedule_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
