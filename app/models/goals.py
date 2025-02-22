from pydantic import BaseModel, Field
from typing import List


class Goals(BaseModel):
    id_User: str
    protein_goal: int = Field(ge=0, le=200, default=0)
    carbs_goal: int = Field(ge=0, le=5000, default=0)
    sodium_goal: int = Field(ge=0, le=5000, default=0)
    fats_goal: int = Field(ge=0, le=5000, default=0)
    calorie_goal: int = Field(ge=0, le=5000, default=0)
