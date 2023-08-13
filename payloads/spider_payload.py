from pydantic import BaseModel
from models.enums import GameStatus, SuitsEnum

class SpiderCreate(BaseModel):
    Suits: SuitsEnum | None = None

class SpiderUpdate(BaseModel):
    Moves: int | None = None
    Elapsed: int | None = None
    Status: GameStatus | None = None