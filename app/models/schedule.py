from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class FoodConsumed(BaseModel):
    food_id: str
    quantity: float = Field(gt=0)


class Schedule(BaseModel):
    id_user: str
    day: str
    foodList: List[FoodConsumed]
