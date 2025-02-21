from pydantic import BaseModel, Field
from typing import List


class Drink(BaseModel):
    name: str
    sugar_portion: float = Field(ge=0, default=0)
    caffeine_portion: float = Field(ge=0, default=0)
    calories_portion: float = Field(ge=0, default=0)
    measure_portion: float = Field(ge=0, default=0)
    measure: str
    typeOfDrink: str
    id_User: str
