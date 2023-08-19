from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from .word_response import WordResponse
from typing import List, Any

class HangManResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Correct: str
    Wrong: str
    Score: int
    Status: GameStatus
    user_id: int | None
    word_id: int | None

    user: UserResponse | None
    word: WordResponse | None

class HangManPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[HangManResponse]

class HangManGuessResponse(BaseModel):
    Letter: str
    Found: bool
