from app.service.category_service import create_category, get_user_categories, update_category, delete_category_service
from app.models.category import Category
from fastapi import HTTPException


def userCategoryLog(category: create_category):
    response = create_category(category)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])


def get_category(user_id: str):
    response = get_user_categories(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def update_category_controller(category_id: str, updated_category: Category):
    response = update_category(category_id, updated_category)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


def delete_category(category_id: str):
    response = delete_category_service(category_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
