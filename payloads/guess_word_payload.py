from pydantic import BaseModel
from typing import List

class GuessWordCreate(BaseModel):
    WordId: int | None = None

class GuessWordGuessPayload(BaseModel):
    Word: str | None = None
    Guess: str | None = None

class GuessWordHint(BaseModel):
    Length: int 
    Green: List[str]
    Brown: List[List[str]]
    Gray: List[str]
