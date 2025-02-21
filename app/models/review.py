from pydantic import BaseModel, Field
from typing import List


class Comment(BaseModel):
    comment: str
    id_User: str
    score: int = Field(ge=0, le=5)


class Update_Review(BaseModel):
    plate_Id: str
    comments: List[Comment]
    score: float = Field(ge=0, le=5)


class Review(BaseModel):
    plate_Id: str
    comments: List = []
    score: float = 0
