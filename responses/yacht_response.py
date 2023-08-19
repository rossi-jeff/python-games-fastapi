from payloads.yacht_payload import YachtOption
from pydantic import BaseModel
from typing import List, Any
from .user_response import UserResponse
from .yacht_turn_response import YachtTurnResponse


class YachtResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Total: int
    NumTurns: int
    user_id: int | None

    user: UserResponse | None
    turns: List[YachtTurnResponse] = []


class YachtPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[YachtResponse]


class YachtRollResponse(BaseModel):
    Turn: YachtTurnResponse
    Options: List[YachtOption]
