from pydantic import BaseModel, Field

# Modelo para registrar un nuevo Food
class Food(BaseModel):
    name: str
    calories_portion: float = Field(..., ge=0)  # Ensure Food_price is non-negative
    measure: str
    measure_portion: float = Field(..., ge=0)
