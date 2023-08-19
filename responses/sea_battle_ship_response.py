from pydantic import BaseModel
from typing import List
from models.enums import ShipType, Navy
from .sea_battle_ship_grid_point_response import SeaBattleShipGridPointResponse
from .sea_battle_ship_hit_response import SeabattleShipHitResponse

class SeaBattleShipResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Type: ShipType
    Navy: Navy
    Size: int
    Sunk: bool
    sea_battle_id: int

    points: List[SeaBattleShipGridPointResponse]
    hits: List[SeabattleShipHitResponse]

