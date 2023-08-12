from pydantic import BaseModel
from models.enums import GameStatus

class ConcentrationUpdate(BaseModel):
    Moves: int | None = None
    Matched: int | None = None
    Elapsed: int | None = None
    Status: GameStatus | None = None