from pydantic import BaseModel
from models.enums import GameStatus

class FreeCellUpdate(BaseModel):
    Moves: int | None = None
    Elapsed: int | None = None
    Status: GameStatus | None = None