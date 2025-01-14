from app.service.user_service import create_user, delete_user, reset_password, get_user_by_id, get_user_by_email, send_password_reset_email, login_user, get_current_user_service, update_user
from app.models.user import UserLogin, ResetPassword, UserRegister, UserForgotPassword, UpdateUserData
from fastapi import HTTPException, Request


def login(user: UserLogin):
    return {"message": "Login successful"}
# Controlador para registrar un nuevo usuario


def userLog(user: UserRegister):
    response = create_user(user)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully"}


def delete_user_by_id(user_id: str):
    response = delete_user(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully"}


def resetPassword(reset: ResetPassword):
    response = reset_password(reset)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Password change successfully"}


# Controlador para recuperación de contraseña
def forgot_password(user: UserForgotPassword):
    db_user = user_by_email(user.email)

    if db_user:  # If user exists in Firestore
        return send_password_reset_email(user.email)
    else:
        raise HTTPException(status_code=404, detail="Email not found")


def user_by_email(email: str):
    response = get_user_by_email(email)

    # If user not found, get_user_by_email returns None
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")

    # If an error occurred during the query
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response


def user_by_id(user_id: str):
    response = get_user_by_id(user_id)

    # If user not found, get_user_by_email returns None
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")

    # If an error occurred during the query
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response


def login_user_controller(user: UserLogin):
    response = login_user(user)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Log in succesful"}


def get_current_user(request: Request):
    response = get_current_user_service(request)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Log in succesful"}


def update_user_info(user_id: str, user_data: UpdateUserData):
    response = update_user(user_id, user_data)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
