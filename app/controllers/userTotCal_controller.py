from app.service.userTotCal_service import updateDailyCalories,createUserTotCal_service,get_totalCAL
from app.models.userFood import UserFood
from fastapi import HTTPException
from datetime import datetime

def updateDailyCalories_controller(calPerDay_id, calUpdate):
    response = updateDailyCalories(calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def createUserTotCal(userTotCal):
    response = createUserTotCal_service(userTotCal)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def get_TotCal(user_id):
    response = get_totalCAL(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}