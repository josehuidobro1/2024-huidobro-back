from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class FoodConsumed(BaseModel):
    food_id: str
    quantity: int


class Schedule(BaseModel):
    id_user: str
    day: str
    foodList: List[FoodConsumed]
