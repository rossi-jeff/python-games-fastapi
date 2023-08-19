from pydantic import BaseModel

class SeaBattleShipGridPointResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Horizontal: str
    Vertical: int
    sea_battle_ship_id: int
