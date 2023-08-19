from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from typing import List, Any


class KlondikeResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Moves: int
    Elapsed: int
    Status: GameStatus
    user_id: int | None

    user: UserResponse | None


class KlondikePaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[KlondikeResponse]
