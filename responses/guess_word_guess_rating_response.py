from pydantic import BaseModel
from models.enums import Rating
from typing import Any

class GuessWordGuessRatingResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    guess_word_guess_id: int
    Rating: Rating
