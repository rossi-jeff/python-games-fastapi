from pydantic import BaseModel

class HangManCreate(BaseModel):
    WordId: int | None = None

class HangManGuess(BaseModel):
    Word: str | None = None
    Letter: str | None = None
