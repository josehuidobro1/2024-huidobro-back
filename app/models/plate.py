from pydantic import BaseModel, Field
from typing import List


class PlateFood(BaseModel):
    ingredientId: str
    quantity: float = Field(..., ge=0)


class Plate(BaseModel):
    id_User: str
    name: str
    ingredients: List[PlateFood]
    calories_portion: float = Field(ge=0)
    sodium_portion: float = Field(ge=0)
    carbohydrates_portion: float = Field(ge=0)
    fats_portion: float = Field(ge=0)
    protein_portion: float = Field(ge=0)
    image: str
    public: bool = Field(default=False)
    verified: int = Field(default=0)
