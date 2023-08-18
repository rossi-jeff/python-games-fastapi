from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from .word_response import WordResponse
from .guess_word_guess_response import GuessWordGuessResponse
from typing import List

class GuessWordResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Score: int
    Status: GameStatus
    user_id: int
    word_id: int

    user: UserResponse
    word: WordResponse
    guesses: List[GuessWordGuessResponse]

class GuessWordPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[GuessWordResponse]
