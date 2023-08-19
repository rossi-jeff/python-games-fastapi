from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from typing import List

class ConcentrationResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Moves: int
    Matched: int
    Elapsed: int
    Status: GameStatus
    user_id: int

    user: UserResponse

class ConcentrationPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[ConcentrationResponse]
