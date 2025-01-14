from pydantic import BaseModel, Field
from datetime import datetime

# Modelo para registrar un nuevo Food


class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    weight: float = Field(..., ge=0)
    height: float = Field(..., ge=0)
    birthDate: datetime


class UserForgotPassword(BaseModel):
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class ResetPassword(BaseModel):
    token: str
    new_password: str


class UpdateUserData(BaseModel):
    id_user: str
    name: str
    surname: str
    weight: float
    height: float
    birthDate: datetime
