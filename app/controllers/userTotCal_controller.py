from app.service.userTotCal_service import updateDailyCalories, createUserTotCal_service, get_totalCAL, count_recent_consecutive_days_with_calories
from app.models.userTotCal import CalUpdateModel, UserTotCal
from fastapi import HTTPException
from datetime import datetime


def validate_date(date, label):
    if date.date() > datetime.now().date():
        raise HTTPException(
            status_code=400, detail=f"{label} must be a date in the past.")


def validate_limit(campo, minimo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo < campo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be grater than {minimo} ")


def updateDailyCalories_controller(calPerDay_id, calUpdate: UserTotCal):
    response = updateDailyCalories(calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def createUserTotCal(id_user: str, userTotCal: UserTotCal):
    if (id_user != userTotCal.id_user):
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    validate_date(userTotCal.day, 'day')
    validate_limit(userTotCal.totCal, 0, 'totCal')
    validate_limit(userTotCal.totProt, 0, 'totProt')
    validate_limit(userTotCal.totSodium, 0, 'totSodium')
    validate_limit(userTotCal.totCarbs, 0, 'totCarbs')
    validate_limit(userTotCal.totFats, 0, 'totFats')
    response = createUserTotCal_service(userTotCal)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def get_TotCal(user_id: str):
    response = get_totalCAL(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def get_streak(user_id: str):
    response = count_recent_consecutive_days_with_calories(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
