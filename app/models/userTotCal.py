from pydantic import BaseModel, Field
from datetime import datetime
# Modelo para registrar un nuevo Food


class UserTotCal(BaseModel):
    id_user: str
    day: datetime
    totCal: float = Field(..., ge=0)
    totProt: float = Field(..., ge=0)
    totSodium: float = Field(..., ge=0)
    totCarbs: float = Field(..., ge=0)
    totFats: float = Field(..., ge=0)


class CalUpdateModel(BaseModel):
    calUpdate: int = Field(ge=0)
