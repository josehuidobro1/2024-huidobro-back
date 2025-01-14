from pydantic import BaseModel, Field
from datetime import datetime
# Modelo para registrar un nuevo Food
class UserTotCal(BaseModel):
    id_user: str
    day: datetime # Ensure Food_price is non-negative
    totCal: float = Field(..., ge=0)