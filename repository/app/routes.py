from fastapi import APIRouter, Depends, Request, HTTPException
from app.models.food import Food
from app.controllers.user_controller import update_user_info, delete_user_by_id, user_by_id, resetPassword
from app.controllers.food_controller import register_new_food, get_foods, get_food_by_id
from app.controllers.userTotCal_controller import updateDailyCalories_controller,createUserTotCal,get_TotCal
from app.controllers.category_controller import userCategoryLog, get_category, update_category_controller, delete_category
from app.controllers.catFood_controller import CategoryFoodLog, get_Food_perCat, delete_Catfood, delete_AllCatfoodByCategory
from app.models.user import UserRegister, ResetPassword, UserForgotPassword, UserLogin, UpdateUserData
# from app.controllers.user_controller import
from app.models.catFood import CategoryFood
from app.models.category import Category
from app.models.userFood import UserFood
from app.models.userTotCal import UserTotCal
from app.controllers.foodUser_controller import update_userFood_controller, userFoodLog, get_meals_user, delete_meal
from datetime import datetime
from .config import verify_token


router = APIRouter()

# Define a simple root endpoint


@router.get("/",tags=["General"])
def read_main():
    return {"msg": "Server is running"}


@router.get("/User/{user_id}",tags=["User"])
async def get_user(user_id: str):
    return user_by_id(user_id)


@router.put("/reset_password/{token}",tags=["User"])
async def reset_password(data: ResetPassword):
    return resetPassword(data)


@router.delete("/delete_user/{id_user}",tags=["User"])
async def delete_user(id_user: str):
    delete_user_by_id(id_user)
    return {"message": "User Delete succefully!"}


@router.post("/Food_log/",tags=["Food"])
async def register_food(Food: Food):
    # user_id = verify_token(token)
    # if not user_id:
    #      raise HTTPException(status_code=403, detail="Invalid token")
    register_new_food(Food)
    return {"message": "Food log added!"}


@router.get("/Foods/",tags=["Food"])
async def read_food_logs():
    return get_foods()


@router.get("/Foods/{food_id}",tags=["Food"])
async def get_food(food_id: str):
    return get_food_by_id(food_id)


async def get_current_user(request: Request):
    token = request.headers.get('Authorization').split("Bearer ")[1]
    decoded_token = await verify_token(token)
    return decoded_token


@router.get("/api/user", tags=["User"])
async def get_user_data(current_user: dict = Depends(get_current_user)):
    # Now you have access to the current user
    return {"email": current_user["email"], "uid": current_user["uid"]}


@router.put("/update_user/{user_id}",tags=["User"])
async def update_user_data(user_id: str, user_data: UpdateUserData):
    update_user_info(user_id, user_data)
    return {"message": "User data uploaded! "}


@router.post("/UserFood_log/",tags=["MealUser"])
async def register_foodMeal(FoodUser: UserFood):
    userFoodLog(FoodUser)
    return {"message": "Meal log added!"}


@router.get("/mealUserDay/{user_id}",tags=["MealUser"])
async def get_meal(user_id: str):
    return get_meals_user(user_id)


@router.delete("/DeleteMealUser/{id_UserFood}",tags=["MealUser"])
async def delete_mealUser(id_UserFood: str):
    return delete_meal(id_UserFood)


@router.put("/UpdateUserFood/{userFood_id}",tags=["MealUser"])
async def update_user_food(userFood_id: str, userFood_data: UserFood):
    return update_userFood_controller(userFood_id, userFood_data)


@router.post("/CreateCategory/",tags=["Category"])
async def category_log(category: Category):
    userCategoryLog(category)
    return {"message": "new category!"}


@router.get("/GetCategoryUser/{user_id}",tags=["Category"])
async def get_category_user(user_id: str):
    return get_category(user_id)


@router.put("/UpdateCategroy/{category_id}",tags=["Category"])
async def update_category(category_id: str, updated_category: Category):
    return update_category_controller(category_id, updated_category)


@router.post("/CreateCatFood/",tags=["CategoryFood"])
async def category_log(catFood: CategoryFood):
    CategoryFoodLog(catFood)
    return {"message": "new categoryFood!"}


@router.get("/GetFoodsPerCategory/{id_Category}",tags=["CategoryFood"])
async def get_Food_Percategory(id_Category: str):
    return get_Food_perCat(id_Category)


@router.delete("/DeleteCategory/{id_Category}",tags=["CategoryFood"])
async def delete_category_user(id_Category: str):
    delete_category(id_Category)
    delete_AllCatfoodByCategory(id_Category)
    return {"message": "Category Delete Succefully!"}


@router.delete("/DeleteCatFood/{id_CatFood}" ,tags=["CategoryFood"])
async def delete_catFood_user(id_CatFood: str):
    delete_Catfood(id_CatFood)
    return {"message": "CatFood Delete succefully!"}

@router.post("/CreateTotCaloriesUser/",tags=["Food"])
async def UserTotCal_log(userTotCal: UserTotCal):
    createUserTotCal(userTotCal)
    return {"message": "new Totalcal added!"}


@router.put("/UpdateTotCaloriesUser/{calPerDay_id}", tags=["Food"])
async def UpdateUserTotCal_log(calPerDay_id: str, calUpdate: int):
    response = updateDailyCalories_controller(calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Update successful!"}

@router.get("/GetTotCalUser/{user_id}",tags=["Food"])
async def get_Totcal_user(user_id: str):
    return get_TotCal(user_id)