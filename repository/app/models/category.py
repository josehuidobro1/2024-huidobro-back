from pydantic import BaseModel, Field

# Modelo para registrar un nuevo Food
class Category(BaseModel):
    name: str
    icon: str  # Ensure Food_price is non-negative
    id_User: str