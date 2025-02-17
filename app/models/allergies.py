from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Allergies(BaseModel):
    name: str
    foods_ids: List[str]
