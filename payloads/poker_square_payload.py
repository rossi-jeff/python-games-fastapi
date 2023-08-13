from pydantic import BaseModel
from models.enums import GameStatus

class PokerSquareUpdate(BaseModel):
    Score: int | None = None
    Status: GameStatus | None = None
    