from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from typing import List

class KlondikeResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Moves: int
    Elapsed: int
    Status: GameStatus
    user_id: int

    user: UserResponse

class KlondikePaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[KlondikeResponse]
