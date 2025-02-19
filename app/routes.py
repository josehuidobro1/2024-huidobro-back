from fastapi import APIRouter, Depends, Request, HTTPException
from app.models.food import Food
from app.controllers.schedule_controller import scheduleLog, get_user_schedule, delete_schedule, update_schedule
from app.controllers.allergies_controller import get_allergies, allergieLog, updateAllergie
from app.controllers.user_controller import userLog, addGoal, update_user_info, delete_user_by_id, user_by_id, resetPassword, update_user_validation, get_all_Users
from app.controllers.userTotCal_controller import updateDailyCalories_controller, createUserTotCal, get_TotCal, get_streak
from app.controllers.food_controller import register_new_food, get_foods, get_food_by_id
from app.controllers.category_controller import userCategoryLog, get_category, update_category_controller, delete_category
from app.controllers.catFood_controller import CategoryFoodLog, get_Food_perCat, delete_Catfood, delete_AllCatfoodByCategory
from app.controllers.plate_controller import get_publicPlates_notUser, update_user_plates_to_verified, plateLog, get_plate_user, delete_plate, update_Plate, get_platebyID, get_publicPlates
from app.controllers.plateFood_controller import PlateFoodLog, update_PlateFood_controller, delete_PlateFood, get_plateFood
from app.controllers.drinkType_controller import register_new_drinkType, get_drinkTypes, get_drinkType_by_id, UserDrinkTypes, delete_DrinkType
from app.controllers.review_controller import reviewLog, UpdateReview, get_plateReviews, get_fiveStarReview
from app.controllers.notification_controller import getNotis, NotificationRead, delete_notification
from app.models.user import UserRegister, ResetPassword, UserForgotPassword, UserLogin, UpdateUserData
from app.controllers.drink_controller import register_new_drink, get_drinks, get_drink_by_id, deletedrink, Updatedrink, Grouped_Drinks
# from app.controllers.user_controller import
from app.models.catFood import CategoryFood
from app.models.schedule import Schedule
from app.models.category import Category
from app.models.userFood import UserFood
from app.models.plate import Plate
from app.models.drink import Drink
from app.models.drinkType import DrinkType
from app.models.review import Review
from app.models.plateFood import PlateFood
from app.models.userTotCal import UserTotCal, CalUpdateModel
from app.models.allergies import Allergies
from app.controllers.foodUser_controller import update_userFood_controller, userFoodLog, get_meals_user, delete_meal
from datetime import datetime
from .config import verify_token
from .dependecies import get_current_user

router = APIRouter()


@router.get("/", tags=["General"])
def read_main():
    return {"msg": "Server is running"}


@router.get("/User/{user_id}", tags=["User"])
async def get_user(user_id: str, user=Depends(get_current_user)):
    return user_by_id(user_id)


@router.put("/reset_password/{token}", tags=["User"])
async def reset_password(data: ResetPassword, user=Depends(get_current_user)):
    return resetPassword(data)


@router.delete("/delete_user/{id_user}", tags=["User"])
async def delete_user(id_user: str, user=Depends(get_current_user)):
    delete_user_by_id(id_user)
    return {"message": "User Delete succefully!"}


@router.post("/user/", tags=["User"])
async def register_user(User: UserRegister, user=Depends(get_current_user)):
    response = userLog(User)
    return {"message": "User log added!"}


@router.post("/Food_log/", tags=["Food"])
async def register_food(Food: Food, user=Depends(get_current_user)):
    # user_id = verify_token(token)
    # if not user_id:
    #      raise HTTPException(status_code=403, detail="Invalid token")
    register_new_food(Food)
    return {"message": "Food log added!"}


@router.get("/Foods/", tags=["Food"])
async def read_food_logs(user=Depends(get_current_user)):
    return get_foods()


@router.get("/Foods/{food_id}", tags=["Food"])
async def get_food(food_id: str, user=Depends(get_current_user)):
    return get_food_by_id(food_id)


async def get_current_user(request: Request, user=Depends(get_current_user)):
    token = request.headers.get('Authorization').split("Bearer ")[1]
    decoded_token = await verify_token(token)
    return decoded_token


@router.get("/api/user", tags=["User"])
async def get_user_data(current_user: dict = Depends(get_current_user), user=Depends(get_current_user)):
    # Now you have access to the current user
    return {"email": current_user["email"], "uid": current_user["uid"]}


@router.put("/update_user/{user_id}", tags=["User"])
async def update_user_data(user_id: str, user_data: UpdateUserData, user=Depends(get_current_user)):
    update_user_info(user_id, user_data)
    return {"message": "User data uploaded! "}


@router.post("/UserFood_log/", tags=["MealUser"])
async def register_foodMeal(FoodUser: UserFood, user=Depends(get_current_user)):
    userFoodLog(FoodUser)
    return {"message": "Meal log added!"}


@router.get("/mealUserDay/{user_id}", tags=["MealUser"])
async def get_meal(user_id: str, user=Depends(get_current_user)):
    return get_meals_user(user_id)


@router.delete("/DeleteMealUser/{id_UserFood}", tags=["MealUser"])
async def delete_mealUser(id_UserFood: str, user=Depends(get_current_user)):
    return delete_meal(id_UserFood)


@router.put("/UpdateUserFood/{userFood_id}", tags=["MealUser"])
async def update_user_food(userFood_id: str, userFood_data: UserFood, user=Depends(get_current_user)):
    return update_userFood_controller(userFood_id, userFood_data)


@router.post("/CreateCategory/", tags=["Category"])
async def category_log(category: Category, user=Depends(get_current_user)):
    userCategoryLog(category)
    return {"message": "new category!"}


@router.get("/GetCategoryUser/{user_id}", tags=["Category"])
async def get_category_user(user_id: str, user=Depends(get_current_user)):
    return get_category(user_id)


@router.put("/UpdateCategory/{category_id}", tags=["Category"])
async def update_category(category_id: str, updated_category: Category, user=Depends(get_current_user)):
    return update_category_controller(category_id, updated_category)


@router.post("/CreateCatFood/", tags=["CatFood"])
async def category_log(catFood: CategoryFood, user=Depends(get_current_user)):
    CategoryFoodLog(catFood)
    return {"message": "new categoryFood!"}


@router.get("/GetFoodsPerCategory/{id_Category}", tags=["CatFood"])
async def get_Food_Percategory(id_Category: str, user=Depends(get_current_user)):
    return get_Food_perCat(id_Category)


@router.delete("/DeleteCategory/{id_Category}", tags=["Category"])
async def delete_category_user(id_Category: str, user=Depends(get_current_user)):
    delete_category(id_Category)
    return {"message": "Category Delete Succefully!"}


@router.delete("/DeleteCatFood/{id_CatFood}", tags=["CatFood"])
async def delete_catFood_user(id_CatFood: str, user=Depends(get_current_user)):
    delete_Catfood(id_CatFood)
    return {"message": "CatFood Delete succefully!"}


@router.post("/CreateTotCaloriesUser/", tags=["Food"])
async def UserTotCal_log(userTotCal: UserTotCal, user=Depends(get_current_user)):
    return createUserTotCal(userTotCal)


@router.put("/UpdateTotCaloriesUser/{calPerDay_id}", tags=["Food"])
async def UpdateUserTotCal_log(calPerDay_id: str, calUpdate: UserTotCal, user=Depends(get_current_user)):
    response = updateDailyCalories_controller(calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Update successful!"}


@router.get("/GetTotCalUser/{user_id}", tags=["Food"])
async def get_Totcal_user(user_id: str, user=Depends(get_current_user)):
    return get_TotCal(user_id)
# PLATE ROUTES


@router.post("/CreatePlate/", tags=["Plate"])
async def plate_log(plate: Plate, user=Depends(get_current_user)):
    return plateLog(plate)


@router.get("/GetPlatesUser/{user_id}", tags=["Plate"])
async def get_plateuser(user_id: str, user=Depends(get_current_user)):
    return get_plate_user(user_id)


@router.get("/GetPlateByID/{plate_id}", tags=["Plate"])
async def get_PlateId(plate_id: str, user=Depends(get_current_user)):
    return get_platebyID(plate_id)


@router.get("/GetPlatePublicPlates/", tags=["Plate"])
async def publicPlates(user=Depends(get_current_user)):
    return get_publicPlates()


@router.put("/UpdatePlate/{plate_id}", tags=["Plate"])
async def update_category(plate_id: str, updated_Plate: Plate, user=Depends(get_current_user)):
    return update_Plate(plate_id, updated_Plate)


@router.delete("/DeletePlate/{id_Plate}", tags=["Plate"])
async def delete_plate_user(id_Plate: str, user=Depends(get_current_user)):
    return delete_plate(id_Plate)
# PLATE FOOD


@router.post("/CreatePlateFood/", tags=["PlateFood"])
async def plateFood_log(plateFood: PlateFood, user=Depends(get_current_user)):
    return PlateFoodLog(plateFood)


@router.get("/GetPlateFood/{plateFood_id}", tags=["PlateFood"])
async def get_plateFood_user(plateFood_id: str, user=Depends(get_current_user)):
    return get_plateFood(plateFood_id)


@router.put("/UpdatePlateFood/{id_PlateFood}", tags=["PlateFood"])
async def update_PlateFood(plateFood_id: str, updated_PlateFood: PlateFood, user=Depends(get_current_user)):
    return update_PlateFood_controller(plateFood_id, updated_PlateFood)


@router.delete("/DeletePlateFood/{id_PlateFood}", tags=["PlateFood"])
async def delete_plateFood(id_plate: str, user=Depends(get_current_user)):
    delete_PlateFood(id_plate)
    return {"message": "plate Delete Succefully!"}

# DRINKS


@router.post("/drink_log/", tags=["Drinks"])
async def register_drink(drink: Drink, user=Depends(get_current_user)):
    # user_id = verify_token(token)
    # if not user_id:
    #      raise HTTPException(status_code=403, detail="Invalid token")
    register_new_drink(drink)
    return {"message": "drink log added!"}


@router.get("/GetDrinks/{user_id}", tags=["Drinks"])
async def read_drink_logs(user_id: str, user=Depends(get_current_user)):
    return get_drinks(user_id)


@router.get("/DrinkById/{drink_id}", tags=["Drinks"])
async def get_drink(drink_id: str, user=Depends(get_current_user)):
    return get_drink_by_id(drink_id)


@router.post("/drinkType_log/", tags=["DrinkType"])
async def register_drink(drinkType: DrinkType, user=Depends(get_current_user)):
    # user_id = verify_token(token)
    # if not user_id:
    #      raise HTTPException(status_code=403, detail="Invalid token")
    response = register_new_drinkType(drinkType)
    return response


@router.get("/getDrinkType/", tags=["DrinkType"])
async def read_drink_logs(user=Depends(get_current_user)):
    return get_drinkTypes()


@router.get("/DrinkTypeByID/{drink_id}", tags=["DrinkType"])
async def get_drinkType(drink_id: str, user=Depends(get_current_user)):
    return get_drinkType_by_id(drink_id)


@router.get("/getUserDrinkType/{user_id}", tags=["DrinkType"])
async def get_drinkTypeUser(user_id: str, user=Depends(get_current_user)):
    return UserDrinkTypes(user_id)


@router.delete("/DeleteDrink/{id_drink}", tags=["Drinks"])
async def delete_drink_user(id_drink: str, user=Depends(get_current_user)):
    response = deletedrink(id_drink)
    return {"message": response}


@router.put("/UpdateDrink/{drink_id}", tags=["Drinks"])
async def UpdateUserTotCal_log(drink_id: str, drinkUpdate: Drink, user=Depends(get_current_user)):
    response = Updatedrink(drink_id, drinkUpdate)
    return {"message": response}


@router.delete("/DeleteDrinkType/{drinkType_id}", tags=["DrinkType"])
async def deleteDrinktype(drinkType_id: str, user=Depends(get_current_user)):
    return delete_DrinkType(drinkType_id)


@router.get("/getUserGroupDrinkType/{user_id}", tags=["Drink"])
async def get_GroupeddrinkTypeUser(user_id: str, user=Depends(get_current_user)):
    return Grouped_Drinks(user_id)


@router.post("/newReview/", tags=["Review"])
async def register_newReview(review: Review, user=Depends(get_current_user)):
    response = reviewLog(review)
    return response


@router.put("/UpdateReview/{review_id}", tags=["Review"])
async def Update_Review(review_id: str, ReviewUpdate: Review, user=Depends(get_current_user)):
    response = UpdateReview(review_id, ReviewUpdate)
    return {"message": response}


@router.get("/PlateReviews/", tags=["Review"])
async def get_reviews(user=Depends(get_current_user)):
    return get_plateReviews()


@router.get("/Streak/{user_id}", tags=["gaminfication"])
async def get_streakuser(user_id: str, user=Depends(get_current_user)):
    return get_streak(user_id)


@router.get("/fivestarReview/{user_id}", tags=["gaminfication"])
async def get_fivestarReviewuser(user_id: str, user=Depends(get_current_user)):
    return get_fiveStarReview(user_id)


@router.get("/updateUsersandPlateVerification/", tags=["gamification"])
def scheduled_verification_task(user=Depends(get_current_user)):
    users = get_all_Users()
    for user in users:
        # Access 'id_user' using dictionary key
        update_user_plates_to_verified(user['id_user'])
        update_user_validation(user['id_user'])


@router.get("/getUserNotifications/{user_id}", tags=["notis"])
def getUser_Notifications(user_id: str, user=Depends(get_current_user)):
    return getNotis(user_id)


@router.put("/markNotificationAsRead/{notification_id}", tags=["Review"])
async def markAsRead(notification_id: str, user=Depends(get_current_user)):
    response = delete_notification(notification_id)
    return {"message": response}


@router.get("/PublicplatesNotFromUser/{user_id}", tags=['Plate'])
def getNotUser_Publicplates(user_id: str, user=Depends(get_current_user)):
    response = get_publicPlates_notUser(user_id)
    return response


@router.get("/addGoal/{user_id}", tags=['gamification'])
def addGoal_Touser(user_id: str, goal_id: int, user=Depends(get_current_user)):
    response = addGoal(user_id, goal_id)
    return response


@router.get("/allergies", tags=['Allergies'])
def get_allAlergies(user=Depends(get_current_user)):
    response = get_allergies()
    return response


@router.post("/allergie/", tags=["Allergies"])
async def register_allergie(allergie: Allergies, user=Depends(get_current_user)):
    response = allergieLog(allergie)
    return response


@router.put("/allergie/{allergie_id}", tags=["Allergies"])
async def Update_Allergie(allergie_id: str, EditAllergie: Allergies, user=Depends(get_current_user)):
    response = updateAllergie(allergie_id, EditAllergie)
    return {"message": response}


@router.get("/schedule/{user_id}", tags=['Schedule'])
def get_schedule(user_id, user=Depends(get_current_user)):
    response = get_user_schedule(user_id)
    return response


@router.post("/schedule/", tags=["Schedule"])
async def create_schedule(schedule: Schedule, user=Depends(get_current_user)):
    response = scheduleLog(schedule)
    return response


@router.put("/schedule/{id}", tags=["Schedule"])
async def update_schedule_data(id: str, EditSchedule: Schedule, user=Depends(get_current_user)):
    response = update_schedule(id, EditSchedule)
    return {"message": response}


@router.delete("/schedule/{user_id}", tags=["Schedule"])
async def delete_user_schedule(user_id: str, user=Depends(get_current_user)):
    response = delete_schedule(user_id)
    return {"message": response}
