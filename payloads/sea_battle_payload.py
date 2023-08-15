from pydantic import BaseModel
from typing import List
from models.enums import ShipType, Navy

class SeaBattlePoint(BaseModel):
    Horizontal: str
    Vertical: int

class SeaBattleCreate(BaseModel):
    Axis: int

class SeaBattleShipPayload(BaseModel):
    Navy: Navy
    ShipType: ShipType
    Size: int
    Points: List[SeaBattlePoint] | None = None

class SeaBattleFire(BaseModel):
    Navy: Navy
    Horizontal: str | None = None
    Vertical: int | None = None
