from pydantic import BaseModel
from models.enums import ShipType, Navy, Target
from typing import Any


class SeaBattleTurnResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    ShipType: ShipType | None
    Navy: Navy
    Target: Target
    Horizontal: str
    Vertical: int
    sea_battle_id: int
