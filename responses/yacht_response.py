from pydantic import BaseModel
from typing import List
from .user_response import UserResponse
from.yacht_turn_response import YachtTurnResponse
from payloads.yacht_payload import YachtOption

class YachtResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Total: int
    NumTurns: int
    user_id: int
    
    user: UserResponse
    turns: List[YachtTurnResponse]

class YachtPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[YachtResponse]

class YachtRollResponse(BaseModel):
    Turn: YachtTurnResponse
    Options: List[YachtOption]
