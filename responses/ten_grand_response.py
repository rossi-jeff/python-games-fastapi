from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from .ten_grand_turn_response import TenGrandTurnResponse
from typing import List
from payloads.ten_grand_payload import TenGrandScoreOption

class TenGrandResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Score: int
    Status: GameStatus
    user_id: int

    user: UserResponse
    turns: List[TenGrandTurnResponse]

class TenGrandPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[TenGrandResponse]

class TenGrandOptionsResponse(BaseModel):
    Dice: List[int]
    Options: List[TenGrandScoreOption]
