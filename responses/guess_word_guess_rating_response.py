from pydantic import BaseModel
from models.enums import Rating

class GuessWordGuessRatingResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    guess_word_guess_id: int
    Rating: Rating
