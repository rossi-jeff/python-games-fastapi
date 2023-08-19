from pydantic import BaseModel
from models.enums import GameStatus, SuitsEnum
from .user_response import UserResponse
from typing import List, Any


class SpiderResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Suits: SuitsEnum
    Moves: int
    Elapsed: int
    Status: GameStatus
    user_id: int | None

    user: UserResponse | None


class SpiderPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[SpiderResponse]
