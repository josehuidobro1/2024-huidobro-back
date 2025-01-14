from app.service.catFood_service import create_categoryFood, getFood_category,delete_catFood,delete_cateFoodByCategory
from app.models.catFood import CategoryFood
from fastapi import HTTPException

def CategoryFoodLog(category: CategoryFood):
    response = create_categoryFood(category)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
def get_Food_perCat(id_Category: str):
    response = getFood_category(id_Category)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}
def delete_Catfood(id_CatFood: str):
    response = delete_catFood(id_CatFood)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
def delete_AllCatfoodByCategory(id_Category: str):
    response = delete_cateFoodByCategory(id_Category)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])