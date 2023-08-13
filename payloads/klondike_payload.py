from pydantic import BaseModel
from models.enums import GameStatus

class KlondikeUpdate(BaseModel):
    Moves: int | None = None
    Elapsed: int | None = None
    Status: GameStatus | None = None