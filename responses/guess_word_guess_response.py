from pydantic import BaseModel
from typing import List
from .guess_word_guess_rating_response import GuessWordGuessRatingResponse

class GuessWordGuessResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    guess_word_id: int
    Guess: str

    ratings: List[GuessWordGuessRatingResponse]
