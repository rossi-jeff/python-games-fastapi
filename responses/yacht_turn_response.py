from pydantic import BaseModel
from models.enums import YachtCategory
from typing import Any


class YachtTurnResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    RollOne: str
    RollTwo: str
    RollThree: str
    Score: int
    Category: YachtCategory | None
    yacht_id: int
