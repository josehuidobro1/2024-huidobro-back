from fastapi import APIRouter, Depends, Request, HTTPException, Security
from app.models.food import Food
from app.controllers.schedule_controller import scheduleLog, get_user_schedule, delete_schedule, update_schedule
from app.controllers.allergies_controller import get_allergies, allergieLog, updateAllergie
from app.controllers.user_controller import userLog, login, addGoal, update_user_info, delete_user_by_id, user_by_id, resetPassword, update_user_validation, get_all_Users
from app.controllers.userTotCal_controller import updateDailyCalories_controller, createUserTotCal, get_TotCal, get_streak
from app.controllers.food_controller import register_new_food, get_foods, get_food_by_id
from app.controllers.category_controller import userCategoryLog, get_category, update_category_controller, delete_category
from app.controllers.catFood_controller import CategoryFoodLog, get_Food_perCat, delete_Catfood, delete_AllCatfoodByCategory
from app.controllers.plate_controller import get_publicPlates_notUser, update_plate_controller, update_user_plates_to_verified, plateLog, get_plate_user, delete_plate, update_Plate, get_platebyID, get_publicPlates
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
from app.models.review import Review, Update_Review
from app.models.plateFood import PlateFood
from app.models.userTotCal import UserTotCal, CalUpdateModel
from app.models.allergies import Allergies
from app.controllers.foodUser_controller import update_userFood_controller, userFoodLog, get_meals_user, delete_meal
from datetime import datetime
from .config import verify_token
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.auth import validate_user_id


auth_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def get_token_from_header(request: Request):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        print('Authorization ', authorization)
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid Authorization header format")
    token = authorization.split(" ")[1]
    return {"token": token}


@router.get("/", tags=["General"])
def read_main(request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return {"msg": "Server is running"}


@router.post("/user/{user_id}", tags=["User"])
async def register_user(user_id: str, User: UserRegister, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    validate_user_id(jwt, user_id)
    userLog(User)
    return {"message": "User log added!"}


@router.get("/User/{user_id}", tags=["User"])
async def get_user(user_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = user_by_id(user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": response}


@router.put("/update_user/{user_id}", tags=["User"])
async def update_user_data(user_id: str, user_data: UpdateUserData, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        print(user)
        update_user_info(user_id, user_data)
        return {"message": "User data uploaded! "}


@router.delete("/delete_user/{id_user}", tags=["User"])
async def delete_user(id_user: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    validate_user_id(jwt, id_user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        delete_user_by_id(id_user)
        return {"message": "User Delete succefully!"}


@router.post("/Food_log/", tags=["Food"])
async def register_food(Food: Food, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    register_new_food(Food)
    return {"message": "Food log added!"}


@router.get("/Foods/", tags=["Food"])
async def read_food_logs(request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return get_foods()


@router.get("/Foods/{food_id}", tags=["Food"])
async def get_food(food_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return get_food_by_id(food_id)

# ------------------------ MEAL ---------------------------


@router.post("/UserFood_log/", tags=["MealUser"])
async def register_foodMeal(FoodUser: UserFood, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = user_by_id(FoodUser.id_User)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    userFoodLog(FoodUser)
    return {"message": "Meal log added!"}


@router.get("/mealUserDay/{user_id}", tags=["MealUser"])
async def get_meal(user_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = user_by_id(user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return get_meals_user(user_id)


@router.delete("/DeleteMealUser/{id_UserFood}", tags=["MealUser"])
async def delete_mealUser(id_UserFood: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid token: user_id not found"
        )
    return delete_meal(user_id, id_UserFood)


@router.put("/UpdateUserFood/{userFood_id}", tags=["MealUser"])
async def update_user_food(userFood_id: str, userFood_data: UserFood, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid token: user_id not found"
        )
    return update_userFood_controller(user_id, userFood_id, userFood_data)


@router.post("/CreateCategory/", tags=["Category"])
async def category_log(category: Category, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid token: user_id not found"
        )
    userCategoryLog(user_id, category)
    return {"message": "new category!"}


@router.get("/GetCategoryUser/{user_id}", tags=["Category"])
async def get_category_user(user_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if user_id not in [id_user, "default"]:
        raise HTTPException(
            status_code=400,
            detail="User id is not correct"
        )
    return get_category(user_id)


@router.put("/UpdateCategory/{category_id}", tags=["Category"])
async def update_category(category_id: str, updated_category: Category, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return update_category_controller(id_user, category_id, updated_category)


@router.delete("/DeleteCategory/{id_Category}", tags=["Category"])
async def delete_category_user(id_Category: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    delete_category(id_user, id_Category)
    return {"message": "Category Delete Succefully!"}

    # --------------------------- TOTAL CALORIES ---------------------------------------


@router.post("/CreateTotCaloriesUser/", tags=["Food"])
async def UserTotCal_log(userTotCal: UserTotCal, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return createUserTotCal(id_user, userTotCal)


@router.put("/UpdateTotCaloriesUser/{calPerDay_id}", tags=["Food"])
async def UpdateUserTotCal_log(calPerDay_id: str, calUpdate: UserTotCal):
    response = updateDailyCalories_controller(calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Update successful!"}


@router.get("/GetTotCalUser/{user_id}", tags=["Food"])
async def get_Totcal_user(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return get_TotCal(user_id)

# __________________________________ PLATES __________________________________


@router.post("/CreatePlate/", tags=["Plate"])
async def plate_log(plate: Plate, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if plate.id_User != id_user:
        raise HTTPException(status_code=400, detail="Id user is not valid")
    return plateLog(plate)


@router.get("/GetPlatesUser/{user_id}", tags=["Plate"])
async def get_plateuser(user_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if user_id != id_user:
        raise HTTPException(status_code=400, detail="Id user is not valid")
    return get_plate_user(user_id)


@router.get("/GetPlateByID/{plate_id}", tags=["Plate"])
async def get_PlateId(plate_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    return get_platebyID(plate_id)


@router.get("/GetPlatePublicPlates/", tags=["Plate"])
async def publicPlates(request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")

    return get_publicPlates()


@router.put("/UpdatePlate/{plate_id}", tags=["Plate"])
async def update_plate_data(plate_id: str, updated_Plate: Plate, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return update_plate_controller(id_user, plate_id, updated_Plate)


@router.delete("/DeletePlate/{id_Plate}", tags=["Plate"])
async def delete_plate_user(id_Plate: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return delete_plate(id_user, id_Plate)

# _________________________________ Drinks __________________________________


@router.post("/drink_log/", tags=["Drinks"])
async def register_drink(drink: Drink, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    register_new_drink(id_user, drink)
    return {"message": "drink log added!"}


@router.get("/GetDrinks/{user_id}", tags=["Drinks"])
async def read_drink_logs(user_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail="The user id is not valid")
    return get_drinks(user_id)


@router.get("/DrinkById/{drink_id}", tags=["Drinks"])
async def get_drink(drink_id: str, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return get_drink_by_id(id_user, drink_id)


@router.post("/drinkType_log/", tags=["DrinkType"])
async def register_drink(drinkType: DrinkType, request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")
    user = verify_token(jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    response = register_new_drinkType(id_user, drinkType)
    return response


@router.get("/getDrinkType/", tags=["DrinkType"])
async def read_drink_logs(request: Request):
    headers = request.headers
    jwt = headers.get('Authorization')
    if not jwt:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")

    return get_drinkTypes()


@router.get("/getUserDrinkType/{user_id}", tags=["DrinkType"])
async def get_drinkTypeUser(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    if user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    return UserDrinkTypes(user_id)


@router.delete("/DeleteDrink/{id_drink}", tags=["Drinks"])
async def delete_drink_user(id_drink: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    response = deletedrink(id_user, id_drink)
    return {"message": response}


@router.put("/UpdateDrink/{drink_id}", tags=["Drinks"])
async def UpdateUserTotCal_log(drink_id: str, drinkUpdate: Drink, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    response = Updatedrink(id_user, drink_id, drinkUpdate)
    return {"message": response}


@router.get("/getUserGroupDrinkType/{user_id}", tags=["Drink"])
async def get_GroupeddrinkTypeUser(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    return Grouped_Drinks(user_id)


@router.get("/Streak/{user_id}", tags=["gamification"])
async def get_streakuser(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user or user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    return get_streak(user_id)


@router.delete("/DeleteDrinkType/{drinkType_id}", tags=["DrinkType"])
async def deleteDrinktype(drinkType_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return delete_DrinkType(id_user, drinkType_id)


@router.post("/newReview/", tags=["Review"])
async def register_newReview(review: Review, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = reviewLog(review)
    return response


@router.put("/UpdateReview/{review_id}", tags=["Review"])
async def update_Review(review_id: str, ReviewUpdate: Update_Review, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = UpdateReview(review_id, ReviewUpdate)
    return {"message": response}


@router.get("/PlateReviews/", tags=["Review"])
async def get_reviews(request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    return get_plateReviews()


@router.get("/getUserNotifications/{user_id}", tags=["notis"])
async def getUser_Notifications(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user or user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    return getNotis(user_id)


@router.delete("/markNotificationAsRead/{notification_id}", tags=["Review"])
async def markAsRead(notification_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    response = delete_notification(id_user, notification_id)
    return {"message": response}


@router.post("/allergie/", tags=["Allergies"])
async def register_allergie(allergie: Allergies, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = allergieLog(allergie)
    return response


@router.put("/allergie/{allergie_id}", tags=["Allergies"])
async def Update_Allergie(allergie_id: str, EditAllergie: Allergies, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = updateAllergie(allergie_id, EditAllergie)
    return {"message": response}


@router.get("/allergies", tags=['Allergies'])
def get_allAlergies(request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = get_allergies()
    return response


@router.get("/addGoal/{user_id}", tags=['gamification'])
def addGoal_Touser(user_id: str, goal_id: int, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    response = addGoal(user_id, goal_id)
    return response


@router.get("/PublicplatesNotFromUser/{user_id}", tags=['Plate'])
def getNotUser_Publicplates(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    response = get_publicPlates_notUser(user_id)
    return response


@router.get("/schedule/{user_id}", tags=['Schedule'])
def get_schedule(user_id, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    response = get_user_schedule(user_id)
    return response


@router.post("/schedule/", tags=["Schedule"])
async def create_schedule(schedule: Schedule, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != schedule.id_user:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    response = scheduleLog(schedule)
    return response


@router.put("/schedule/{id}", tags=["Schedule"])
async def update_schedule_data(id: str, EditSchedule: Schedule, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    id_user = user.get("user_id")
    if id_user != EditSchedule.id_user:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    response = update_schedule(id, EditSchedule)
    return {"message": response}


@router.delete("/schedule/{user_id}", tags=["Schedule"])
async def delete_user_schedule(user_id: str, request: Request):
    user = verify_token(request.headers.get("Authorization"))
    if not user or user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    id_user = user.get("user_id")
    if id_user != user_id:
        raise HTTPException(
            status_code=400, detail=f"User id is not valid")
    response = delete_schedule(user_id)
    return {"message": response}
