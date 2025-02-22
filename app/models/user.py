from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

# Modelo para registrar un nuevo Food


class UserGoals(BaseModel):
    calories: int = Field(ge=0, le=5000, default=0)
    sodium: int = Field(ge=0, le=3000, default=0)
    fats: int = Field(ge=0, le=100, default=0)
    carbohydrates: int = Field(ge=0, le=400, default=0)
    protein: int = Field(ge=0, le=500, default=0)
    sugar: int = Field(ge=0, le=100, default=0)
    caffeine: int = Field(ge=0, le=600, default=0)


class UserRegister(BaseModel):
    id_user: str
    name: str
    surname: str
    weight: float = Field(ge=0, le=500)
    height: float = Field(ge=0, le=500)
    birthDate: datetime
    goals: UserGoals
    validation: int = Field(default=0)
    achievements: List[int]
    allergies: List[str]


class UserForgotPassword(BaseModel):
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class ResetPassword(BaseModel):
    token: str
    new_password: str


class UpdateUserData(BaseModel):
    name: str
    surname: str
    weight: float
    height: float
    birthDate: datetime
    goals: UserGoals
    validation: int = Field(default=0)
    achievements: List[int]
    allergies: List[str]
