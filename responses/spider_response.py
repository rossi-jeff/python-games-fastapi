from pydantic import BaseModel
from models.enums import GameStatus, SuitsEnum
from .user_response import UserResponse
from typing import List

class SpiderResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Suits: SuitsEnum
    Moves: int
    Elapsed: int
    Status: GameStatus
    user_id: int

    user: UserResponse

class SpiderPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[SpiderResponse]
