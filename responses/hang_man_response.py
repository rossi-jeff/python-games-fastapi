from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from .word_response import WordResponse
from typing import List

class HangManResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Correct: str
    Wrong: str
    Score: int
    Status: GameStatus
    user_id: int
    word_id: int

    user: UserResponse
    word: WordResponse

class HangManPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[HangManResponse]

class HangManGuessResponse(BaseModel):
    Letter: str
    Found: bool
