from pydantic import BaseModel, Field
from datetime import datetime


class UserNotification(BaseModel):
    is_read: bool = Field(default=False)
    message: str
    timestamp: datetime
    user_id: str
