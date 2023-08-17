from pydantic import BaseModel
from typing import List
from models.enums import YachtCategory

class YachtRoll(BaseModel):
    Keep: List[int]

class YachtScore(BaseModel):
    TurnId: int
    Category: YachtCategory

class YachtOption(BaseModel):
    Category: YachtCategory
    Score: int
