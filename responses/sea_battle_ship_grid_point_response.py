from pydantic import BaseModel
from typing import Any


class SeaBattleShipGridPointResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Horizontal: str
    Vertical: int
    sea_battle_ship_id: int
