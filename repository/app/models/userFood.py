from pydantic import BaseModel, Field
from datetime import datetime

class UserFood(BaseModel):
    id_User: str
    id_Food: str
    date_ingested: datetime
    amount_eaten: float = Field(..., ge=0)



