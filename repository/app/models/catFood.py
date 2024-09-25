from pydantic import BaseModel, Field

# Modelo para registrar un nuevo Food
class CategoryFood(BaseModel):
    id_Category: str
    id_Food: str