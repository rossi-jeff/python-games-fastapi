from pydantic import BaseModel
from models.enums import ShipType, Navy, Target

class SeaBattleTurnResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    ShipType: ShipType | None
    Navy: Navy
    Target: Target
    Horizontal: str
    Vertical: int
    sea_battle_id: int
