from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from typing import List

class PokerSquareResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Score: int
    Status: GameStatus
    user_id: int

    user: UserResponse

class PokerSquarePaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[PokerSquareResponse]
