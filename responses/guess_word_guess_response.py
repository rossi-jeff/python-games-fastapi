from pydantic import BaseModel
from typing import List, Any
from .guess_word_guess_rating_response import GuessWordGuessRatingResponse

class GuessWordGuessResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    guess_word_id: int
    Guess: str

    ratings: List[GuessWordGuessRatingResponse] = []
