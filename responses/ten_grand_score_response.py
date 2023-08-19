from pydantic import BaseModel
from models.enums import TenGrandCategory
from typing import Any


class TenGrandScoreResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Dice: str
    Score: int
    Category: TenGrandCategory
    ten_grand_turn_id: int
