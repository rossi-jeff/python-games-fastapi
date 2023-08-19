from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from .word_response import WordResponse
from .guess_word_guess_response import GuessWordGuessResponse
from typing import List, Any

class GuessWordResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Score: int
    Status: GameStatus
    user_id: int | None
    word_id: int | None

    user: UserResponse | None
    word: WordResponse | None
    guesses: List[GuessWordGuessResponse] = []

class GuessWordPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[GuessWordResponse]
