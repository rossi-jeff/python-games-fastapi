from pydantic import BaseModel
from models.enums import GameStatus
from .user_response import UserResponse
from .sea_battle_ship_response import SeaBattleShipResponse
from .sea_battle_turn_response import SeaBattleTurnResponse
from typing import List, Any


class SeaBattleResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Axis: int
    Score: int
    Status: GameStatus
    user_id: int | None

    user: UserResponse | None
    ships: List[SeaBattleShipResponse] = []
    turns: List[SeaBattleTurnResponse] = []


class SeaBattlePaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[SeaBattleResponse]
