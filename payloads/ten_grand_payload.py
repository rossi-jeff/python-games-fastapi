from pydantic import BaseModel
from typing import List
from models.enums import TenGrandCategory

class TenGrandRoll(BaseModel):
    Quantity: int

class TenGrandOptions(BaseModel):
    Dice: List[int]

class TenGrandScoreOption(BaseModel):
    Score: int
    Category: TenGrandCategory

class TenGrandScorePayload(BaseModel):
    TurnId: int
    Dice: List[int]
    Options: List[TenGrandScoreOption]
